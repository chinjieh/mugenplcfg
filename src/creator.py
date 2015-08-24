# Module that handles creation of the XML document
import parseutil
import customExceptions
import util
import paths
import os
import message
import devicecap
import extractor
import subprocess
import shutil
import mmap
import struct
from collections import namedtuple, OrderedDict, deque
from schemadata import Element

Address = namedtuple("Address", "start end")
PAGE_SIZE = "0x1000"  # 4KB
PAGE_MIN_SIZE = PAGE_SIZE
MEM_ALLOCATABLE_MINSIZE = "0x100000"  # 1 MB
PROCESSOR_SPEED_KEYWORDS = ["GHz", "MHz"]


class ProcessorCreator():


    def createElem(self, cpuinfopath, msrpaths):
        print "> Creating element: processor"
        processor = Element("processor", "processorType")
        # Logical Cpus
        processor["logicalCpus"] = self.getLogicalCpus(cpuinfopath)

        # Speed
        processor["speed"] = self.getSpeed(
            cpuinfopath, PROCESSOR_SPEED_KEYWORDS)

        # vmxTimerRate
        VMX_OFFSET = 0x485
        VMX_BITSIZE = 5
        processor["vmxTimerRate"] = self.getVmxTimerRate(msrpaths,
                                                                     VMX_OFFSET,
                                                                     VMX_BITSIZE)
        print "Element created: processor"
        return processor


    def getLogicalCpus(self, cpuinfopath):
        cpuinfo = extractor.extractData(cpuinfopath)
        return parseutil.count(cpuinfo, "processor")


    def getSpeed(self, cpuinfopath, speedkeywords):
        result = "0"

        def handleSpeedNotFound():
            # ProcessorSpeedNotFound
            message.addError(
                "Could not find processor speed in: %s\n" % cpuinfopath +
                "Values do not match speed keywords: %s" % ", ".join(
                    speedkeywords)
            )

        try:
            modelnamedata = parseutil.parseData_Sep(
                extractor.extractData(cpuinfopath),
                "model name", ":")
        except customExceptions.KeyNotFound:
            handleSpeedNotFound()
        tokens = modelnamedata.split()
        speedtoken = None
        for token in tokens:
            for speedtype in speedkeywords:
                if speedtype in token:
                    speedtoken = token
                    break
        if speedtoken is None:
            handleSpeedNotFound()
        else:
            speedvalue = util.getSpeedValue(speedtoken, speedkeywords)
            if speedvalue is None:
                handleSpeedNotFound()
            else:
                result = speedvalue

        return result


    def getVmxTimerRate(self, msrpaths, offset, vmxbitsize):
        # check for MSR
        vmxTimerRate = 0

        MSRfound = False
        for path in msrpaths:
            try:
                # Try to find MSR file
                vmxTimerRate = self.getVmxFromMSR(path, offset, vmxbitsize)
            except IOError:
                pass
            else:
                MSRfound = True
                break
        if not MSRfound:
            # MSRFileNotFound
            errormsg = "MSR could not be located at directories:\n"
            for path in msrpaths:
                errormsg += ("%s\n" % path)

            errormsg += ("vmxTimerRate could not be found. Try 'modprobe msr' to "
                         "probe for MSR, then run the tool again.")
            message.addError(errormsg)

        return vmxTimerRate


    def getVmxFromMSR(self, msrpath, offset, vmxbitsize):
        "Gets VmxTimerRate value from a given msr path"
        # Try to find MSR file
        byte = extractor.extractBinaryData(msrpath, offset, 1)
        # Raises IOError here if not found
        vmxbits = 0
        # Get bits from VMX_BITS_START to VMX_BITS_END
        for bitnum in range(0, vmxbitsize):
            vmxbits += util.getBit(int(byte, 16), bitnum) << bitnum
        vmxTimerRate = int(vmxbits)
        return vmxTimerRate


class MemoryCreator():


    def createElem(self, memmappath):
        print "> Creating element: memory"

        memory = Element("memory", "physicalMemoryType")
        # Get list of memoryBlocks available
        memoryBlockList = self.getMemoryBlocks(memmappath)
        for memoryBlock in memoryBlockList:
            memory.appendChild(memoryBlock)
        print "Element created: memory"
        return memory


    def getMemoryBlocks(self, path):
        memoryBlockList = []

        def walkError(excep):
            message.addError("Could not access memory block data: " +
                             str(excep), False)

        memdirs = []
        for root, subdirs, files in os.walk(path, onerror=walkError):
            if not subdirs:  # at end of paths
                memdirs.append(root)

        memdirs.sort(key=lambda x: int(os.path.basename(x)))
                     # Sort paths found by numerical order
        for root in memdirs:
            endfile = root + "/" + "end"
            typefile = root + "/" + "type"
            startfile = root + "/" + "start"
            try:
                memoryBlock = self.generateMemoryBlock(endfile,
                                                                typefile,
                                                                startfile)
            except IOError:
                message.addError("Could not retrieve complete memory data",
                                 False)
            else:
                # Adds newly created memoryBlock element to memoryBlockList
                memoryBlockList.append(memoryBlock)

        # Filter out memoryBlocks that do not meet requirements
        memoryBlockList = self.filterMemoryBlocks(memoryBlockList)

        return memoryBlockList


    def filterMemoryBlocks(self, memoryBlockList):
        "Removes reserved memory blocks and returns result"
        RESERVE_NAME = "reserved"
        result = []
        print "Filtering memory blocks found..."
        filterlist = [memblock for memblock in memoryBlockList
                      if memblock["name"] == "reserved"]
        result = util.removeListsFromList(memoryBlockList, filterlist)
        return result


    def generateMemoryBlock(self, endfile, typefile, startfile):
        memoryBlock = Element("memoryBlock", "memoryBlockType")
        memoryBlock["name"] = extractor.extractData(typefile)
        memaddr = extractor.extractData(startfile)
        memoryBlock["physicalAddress"] = util.toWord64(memaddr)
        memsize = util.sizeOf(extractor.extractData(endfile),
                              extractor.extractData(startfile))
        # Round memsize down to multiple of PAGE_SIZE
        if int(memsize, 16) % int(PAGE_SIZE, 16) != 0:
            memrounded = util.hexRoundToMultiple(
                memsize, PAGE_SIZE, rounddown=True)
            print "Mem size %s for memoryBlock %s rounded down to: %s" % (
                memsize, memaddr, memrounded)
            memsize = memrounded
        memoryBlock["size"] = util.toWord64(memsize)

        if self.isAllocatable(memoryBlock):
            memoryBlock["allocatable"] = "true"
        else:
            memoryBlock["allocatable"] = "false"

        return memoryBlock


    def isAllocatable(self, memoryBlock):
        addr = int(util.unwrapWord64(memoryBlock["physicalAddress"]), 16)
        if (memoryBlock["name"] == "System RAM" and
                addr >= int(MEM_ALLOCATABLE_MINSIZE, 16)):
            return True
        else:
            return False


class DevicesCreator():


    def createElem(self):
        print "> Creating element: devices"
        devices = Element("devices", "devicesType")
        devices["pciConfigAddress"] = util.toWord64(
            self.getPciConfigAddress(paths.IOMEM)
        )

        # Add IOMMUs
        print "> Extracting IOMMU device information..."
        devices.appendChild(IommuDevicesCreator().createElems())

        # Add Serial Devices
        print "> Extracting Serial device information..."
        devices.appendChild(SerialDevicesCreator().createElems(paths.IOPORTS))

        # Add Pci Devices
        print "> Extracting PCI device information..."
        devices.appendChild(PciDevicesCreator().createElems(paths.DEVICES))

        print "Element created: devices"

        return devices


    def getPciConfigAddress(self, path):
        pciconfigaddr = ""
        key = "PCI MMCONFIG"
        try:
            iomemdata = extractor.extractData(path)
            keyline = parseutil.findLines(iomemdata, key)[0]
            pciconfigaddr = keyline.split("-")[0].lstrip()

        except (customExceptions.KeyNotFound, IOError):
            message.addWarning(
                "Could not obtain pciConfigAddress from %s." % path)

        return pciconfigaddr


class PciDevicesCreator():

    "Helper class of DevicesCreator"

    def __init__(self):
        self.devicenames = {}  # devicepath = name

    def createElems(self, devicesdir):
        pcidevicelist = []
        devicepaths = []
        devicecapmgr = None
        deviceShortNames = {}
        print "Finding PCI devices..."
        # Get device absolute paths from symbolic links in paths.DEVICES
        devicepaths = util.getLinks(devicesdir, self.isDeviceName)
        print "Checking Dependencies..."
        devicecapmgr = self.init_DevicecapManager(devicepaths)
        deviceShortNames = self.getDeviceShortNames(devicepaths, paths.PCIIDS)
        print "Examining PCI devices..."
        filteredpaths = self.filterDevicePaths(devicepaths, devicecapmgr)
        print ("Extracting device information from %d PCI devices " %
               len(filteredpaths) +
               "(excluding PCI bridges and non PCI-Express "
               "devices behind bridges)...")
        for devicepath in filteredpaths:
            pcidevicelist.append(self.createDeviceFromPath(devicepath,
                                                           devicecapmgr,
                                                           deviceShortNames))

        return pcidevicelist

    def init_DevicecapManager(self, devicepaths):
        "Initialises the DeviceCapManager"

        print "Getting device capabilities..."
        devicecapmgr = devicecap.DevicecapManager()
        try:
            devicecapmgr.extractCapabilities(devicepaths)
        except customExceptions.DeviceCapabilitiesNotRead:
            message.addError("Not enough permissions to access capabilities "
                             "of devices. It is advised to run the tool again "
                             "with the proper permissions.", False)
        return devicecapmgr

    def filterDevicePaths(self, devicePaths, devicecapmgr):
        "Returns filtered list of paths of devices"
        bridgePaths = []
        pciExpressPaths = []
        bridgedDevicePaths = []
        nonPciExpressPaths = []
        resultPaths = []
        for devicepath in devicePaths:
            if self.isPciExpress(devicepath, devicecapmgr):
                pciExpressPaths.append(devicepath)

            if self.isBridge(devicepath):
                bridgePaths.append(devicepath)
                for root, subdirs, files in os.walk(devicepath):
                    for subdir in subdirs:
                        if self.isDeviceName(subdir):
                            bridgedDevicePaths.append(
                                os.path.join(root, subdir))

        for bridgedDevice in bridgedDevicePaths:
            if self.isPciExpress(bridgedDevice, devicecapmgr) is False:
                nonPciExpressPaths.append(bridgedDevice)

        print "PCI Devices found: %d\n------------------" % len(devicePaths)
        print "> PCI Bridges: ", len(bridgePaths)
        for item in bridgePaths:
            print "  ", os.path.basename(item)

        print "> Devices behind bridges: ", len(bridgedDevicePaths)
        for item in bridgedDevicePaths:
            print "  ", os.path.basename(item)

        print "> PCI Express Devices: ", len(pciExpressPaths)
        for item in pciExpressPaths:
            print "  ", os.path.basename(item)

        resultPaths = util.removeListsFromList(devicePaths,
                                               bridgePaths,
                                               nonPciExpressPaths)
        return resultPaths

    def isBridge(self, devicepath):
        isBridge = False
        PCI_BRIDGE = "0x0604"
        if extractor.extractData(os.path.join(devicepath, "class"))[0:6] == PCI_BRIDGE:
            isBridge = True

        return isBridge

    def isPciExpress(self, devicepath, devicecapmgr):
        isPciExpress = False
        PCI_EXPRESS = "0x10"

        if PCI_EXPRESS in devicecapmgr.getCapList(devicepath):
            isPciExpress = True

        return isPciExpress

    def isDeviceName(self, value):
        "Checks for format: ####:##:##.#"
        splitcolon = value.split(':')
        result = True

        try:
            if len(splitcolon) != 3:
                result = False

            if '.' not in splitcolon[2]:
                result = False

            if len(splitcolon[0]) != 4:  # Host bus no. length
                result = False

            if len(splitcolon[1]) != 2:  # Bus no. length
                result = False

            if len(splitcolon[2].split('.')[0]) != 2:  # Device no. length
                result = False

            if len(splitcolon[2].split('.')[1]) != 1:  # Function no. length
                result = False
        except IndexError:
            result = False

        return result

    def getDeviceBus(self, devicestr):
        return devicestr.split(':')[1]

    def getDeviceNo(self, devicestr):
        return (devicestr.split(':')[2]).split('.')[0]

    def getDeviceFunction(self, devicestr):
        return (devicestr.split(':')[2]).split('.')[1]

    # TODO Unused for now, while device names are relying on class codes and
    # not Vendor and Device pairs
    """
	@staticmethod
	def getDeviceNames(devicepaths):
		"Gets device names from pci.ids"
		names = {}
		#Initialise names
		for devicepath in devicepaths:
			names[devicepath] = "NO_NAME"

		#Attempt to access pci.ids to retrieve device name
		try:
			pciIdsParser = parseutil.PciIdsParser(paths.PCIIDS)

		except customExceptions.PciIdsFileNotFound:
			message.addError("pci.ids file could not be located in tool directory: "
							 "%s. " % paths.CURRENTDIR + "Device names could not "
							 "be obtained.\nPlease ensure that the file is in "
							 "the directory.", False)

		else:
			for devicepath in devicepaths:
				try:
					venhex = extractor.extractData(os.path.join(devicepath,"vendor") )
					devhex = extractor.extractData(os.path.join(devicepath,"device") )
					names[devicepath] = pciIdsParser.getVendorName(venhex) #TODO Name constraint
				except customExceptions.PciIdsFailedSearch as e:
					message.addWarning(("Names for Device %s of Vendor %s could " +
									   "not be found. ") % (devhex,venhex) +\
									   "It would be a good idea to update pci.ids")

				except customExceptions.PciIdsMultipleEntries as e:
					message.addWarning("Multiple names for Device %s of Vendor %s " %
									   (devhex, venhex) + "were found. Please "
									   "insert the correct names manually in the "
									   "XML file.")

		return names
	"""

    def getDeviceShortNames(self, devicepaths, pciids):
        shortnames = OrderedDict()
        namecount = {}
        try:
        # Initialise PciIdsParser, throws customExceptions.PciIdsFileNotFound
        # if fail
            pciIdsParser = parseutil.PciIdsParser(pciids)
        except customExceptions.PciIdsFileNotFound:
            message.addError("pci.ids file could not be located in tool "
                             "directory: %s. " % paths.CURRENTDIR +
                             "Device "
                             "names could not be obtained. Please ensure that "
                             "the file is in the directory.",
                             False)
        else:

            for devicepath in devicepaths:
                # Add entry to dictionary shortnames
                shortnames[devicepath] = self.getClassName(
                    devicepath, pciIdsParser)

            namelist = []
            for value in shortnames.itervalues():
                namelist.append(value)

            listnumberer = util.ListNumberer(namelist)
            for devicepath in shortnames.iterkeys():
                shortnames[devicepath] = listnumberer.getName(
                    shortnames[devicepath])

        return shortnames

    def getClassName(self, devicepath, pciIdsParser):
        "Checks the pciIdsParser object and gets the class name for the device"
        # Get class code from "class" file"
        classcode = extractor.extractData(
            os.path.join(devicepath, "class"))[0:8]
        classname = classcode
        try:
            classname = pciIdsParser.getClassName(classcode[0:6])
            classname = util.spacesToUnderscores(classname.lower())
        except (customExceptions.PciIdsFailedSearch,
                customExceptions.PciIdsSubclassNotFound):
            message.addWarning(("Name for Device at: %s " % devicepath +
                                "could not be found. It would " +
                                "be a good idea to update pci.ids " +
                                "(try '-update' or '-u')"))
        return classname

    def getPci(self, devicepath, devicecapmgr):
        pcistr = os.path.basename(devicepath)
        pci = Element("pci", "pciType")
        pci["bus", "device", "function"] = (
            util.wrap16(self.getDeviceBus(pcistr)),
            util.wrap16(self.getDeviceNo(pcistr)),
            self.getDeviceFunction(pcistr))

        pci["msi"] = self.getPci_MSI(devicepath, devicecapmgr)

        return pci

    def getPci_MSI(self, devicepath, devicecapmgr):
        msi = "false"
        if devicecap.CAP_MSI in devicecapmgr.getCapList(devicepath):
            if devicecapmgr.getCapValue(devicepath, devicecap.CAP_MSI).enable:
                msi = "true"
        if devicecap.CAP_MSIX in devicecapmgr.getCapList(devicepath):
            if devicecapmgr.getCapValue(devicepath, devicecap.CAP_MSIX).enable:
                msi = "true"

        return msi

    def getIrq(self, devicepath):
        irq = None
        try:
            irqNo = extractor.extractData(os.path.join(devicepath, "irq"))
        except IOError:
            message.addError("Could not obtain irq number for device: %s" %
                             os.path.basename(devicepath), False)
        else:
            if irqNo is not "0":
                irq = Element("irq", "irqType")
                irq["name", "number"] = "irq", irqNo
        return irq

    def getDeviceMemoryBlocks(self, devicepath, minsize=PAGE_MIN_SIZE):
        devmemblocks = []
        try:
            resourceData = extractor.extractData(
                os.path.join(devicepath, "resource"))
        except IOError:
            message.addError("Could not obtain memory information for device: "
                             "%s" % os.path.basename(
                                 devicepath),
                             False)
        else:
            memcount = 0
            for line in resourceData.splitlines():
                tokens = line.split(' ')
                if tokens[2][-3] == '2':  # if line represents a memory block

                    memory = Element("memory", "deviceMemoryType")
                    memory["name"] = "mem%d" % memcount
                    memory["physicalAddress"] = util.toWord64(tokens[0])
                    # Rounds memsize up to minsize
                    memsize = util.sizeOf(tokens[1], tokens[0])
                    if int(memsize, 16) < int(minsize, 16):
                        memrounded = util.hexFloor(memsize, minsize)
                        print ("Mem size %s for device %s rounded to: %s" %
                              (memsize,
                               os.path.basename(devicepath),
                               memrounded))
                        memsize = memrounded

                    memory["size"] = util.toWord64(memsize)
                    memory["caching"] = "UC"  # TODO
                    devmemblocks.append(memory)
                    memcount += 1

        return devmemblocks

    def getIoports(self, devicepath):
        ioports = []

        try:
            resourceData = extractor.extractData(
                os.path.join(devicepath, "resource"))
        except IOError:
            message.addError("Could not obtain ioport information for device: "
                             "%s" % os.path.basename(
                                 devicepath),
                             False)
        else:
            ioportcount = 0
            for line in resourceData.splitlines():
                tokens = line.split(' ')
                if tokens[2][-3] == '1':  # if line represents ioport information

                    ioPort = Element("ioPort", "ioPortType")
                    ioPort["name"] = "ioport%d" % ioportcount
                    ioPort["start"] = util.toWord64(tokens[0])
                    ioPort["end"] = util.toWord64(tokens[1])
                    ioportcount += 1

                    ioports.append(ioPort)
        return ioports

    def createDeviceFromPath(self, devicepath, devicecapmgr, deviceShortNames):
        device = Element("device", "deviceType")
        # Old code that gets device name as Vendor DeviceName
        # device["name"] = self.devicenames[devicepath]
        device["name"] = deviceShortNames[devicepath]
        device[
            "shared"] = "false"  # TODO Check for shared status sometime

        # pci
        device.appendChild(self.getPci(devicepath, devicecapmgr))

        # irq
        device.appendChild(self.getIrq(devicepath))

        # memory, includes expansion roms
        for devmemblock in self.getDeviceMemoryBlocks(devicepath):
            device.appendChild(devmemblock)

        # ioports
        for ioport in self.getIoports(devicepath):
            device.appendChild(ioport)

        # capabilities
        """
		caplist = self.devicecapmgr.getCapList(devicepath)
		if caplist:
			capabilities = Element("capabilities", "capabilitiesType")
			for cap in caplist:
				capability = Element("capability", "capabilityType")
				capability["name"] = cap

				try:
					capability.setContent(devicecap.translate(cap))
				except customExceptions.CapabilityUnknown:
					message.addWarning("Capability code: %s is unknown. " % cap +
									   "It might be a good idea to update "
									   "'devicecap.py'.")
					capability.setContent(cap)

				capabilities.appendChild(capability)

			device.appendChild(capabilities)
		"""

        return device


class SerialDevicesCreator():

    "Helper class of DevicesCreator"

    def __init__(self):
        self.addresses = []
        self.COMADDRESSES = {
            Address("03f8", "03ff"): "com_1",
            Address("02f8", "02ff"): "com_2",
            Address("03e8", "03ef"): "com_3",
            Address("02e8", "02ef"): "com_4"
        }

    def createElems(self, ioportspath):
        serialdevicelist = []
        self.addresses = self.getSerialAddresses(ioportspath)
        # Get COM Device addresses
        for comdevice in self.createComDevices(self.addresses, self.COMADDRESSES):
            serialdevicelist.append(comdevice)

        # Omit non COM serial devices for now
        """
		#Filter COM devices from list
		filteredlist = util.removeListsFromList(self.addresses,
												self.COMADDRESSES.iterkeys() )
		for serialdevice in self.createSerialDevices(filteredlist):
			serialdevicelist.append(serialdevice)
		"""

        return serialdevicelist

    def getSerialAddresses(self, ioportspath):
        "Gets serial addresses in form (startaddr, endaddr)"
        serialAddresses = []
        KEYWORD = "serial"

        # Get all lines which include KEYWORD
        try:
            ioportdata = extractor.extractData(ioportspath)
        except IOError:
            message.addError("Could not access location: %s\n" % ioportspath +
                             "Serial device addresses not found.", False)
        else:
            try:
                lines = parseutil.findLines(ioportdata, KEYWORD)
            except customExceptions.KeyNotFound:
                message.addMessage(
                    "No serial devices found from file: %s" % ioportspath)
            else:
                # Retrieve (start,end) data for serial devices
                for line in lines:
                    serialAddresses.append(self.getAddressFromLine(line))

        print "Serial devices found: %d\n------------------" % len(serialAddresses)
        for addr in serialAddresses:
            print "  Start: ", "0x" + addr.start, " End: ", "0x" + addr.end

        return serialAddresses

    def getAddressFromLine(self, line):
        "Parses line to obtain (start,end)"
        addrInfo = line.partition(":")[0].strip()
        start = addrInfo.partition("-")[0]
        end = addrInfo.partition("-")[2]
        addr = Address(start, end)
        return addr

    def createComDevices(self, serialAddresses, comAddresses):
        "Creates COM devices from those in serialAddresses that match the addr"
        "in comAddresses"
        comdevices = []
        comaddr = []
        for addr in serialAddresses:
            if addr in comAddresses:
                comaddr.append(addr)

        for addr in comaddr:
            device = Element("device", "deviceType")
            device["name"] = comAddresses[addr]
            device["shared"] = "true"
            ioport = Element("ioPort", "ioPortType")
            ioport["name"] = "ioport"
            ioport["start"] = util.toWord64(addr.start)
            ioport["end"] = util.toWord64(addr.end)
            device.appendChild(ioport)
            comdevices.append(device)

        return comdevices

    def createSerialDevices(self, addresses):
        devices = []
        serialcount = 0
        for addr in addresses:
            device = Element("device", "deviceType")
            device["name"] = "serial_%d" % serialcount
            device["shared"] = "true"
            ioport = Element("ioPort", "ioPortType")
            ioport["name"] = "ioport"
            ioport["start"] = util.toWord64(addr.start)
            ioport["end"] = util.toWord64(addr.end)
            device.appendChild(ioport)
            devices.append(device)
            serialcount += 1

        return devices


class IommuDevicesCreator():

    class IommuNamer():

        def __init__(self, iommuaddrs):
            self.iommunames = deque([])
            for addr in iommuaddrs:
                self.iommunames.append("iommu")
            self.iommunames = deque(util.numberMultiples(self.iommunames))

        def getName(self):
            return self.iommunames.popleft()

    def __init__(self):
        pass

    def createElems(self):
        # IASL_CMD_STR = "subprocess.call(['iasl', '-d', '%s'],
        # stdout=subprocess.PIPE)"
        CAPABILITY_OFFSET = "0x08"
        CAP_REG_BYTE_SIZE = 7
        AGAW_BIT_START = 8
        IOMMU_SIZE = "1000"

        elemlist = []
        # outputpath = paths.TEMP
        # tempname = "dmar.dat"
        # parsedname = tempname.split('.')[0] + ".dsl"

        print "> Parsing DMAR table with iasl tool..."
        dmarparser = parseutil.DMARParser()
        # Create parsed copy of DMAR table
        if dmarparser.genDMAR(paths.DMAR,
                              os.path.join(paths.TEMP, "dmar.dat")):
            # iaslcmdstr = IASL_CMD_STR % os.path.join(outputpath,tempname)
            if dmarparser.parseDMAR():
                print "Parsing of DMAR file with iasl successful."
                # Get iommu addresses from DMAR
                iommuaddrs = dmarparser.getIommuAddrs()
                # Instantiate IommuNamer to set names for iommu devices
                iommunamer = self.IommuNamer(iommuaddrs)

                # Create Iommu devices
                for addr in iommuaddrs:
                    elemlist.append(self.createDeviceFromAddr(paths.DEVMEM,
                                                              addr,
                                                              iommunamer,
                                                              IOMMU_SIZE,
                                                              CAPABILITY_OFFSET,
                                                              CAP_REG_BYTE_SIZE,
                                                              AGAW_BIT_START
                                                              )
                                    )

        return elemlist

    """def createElems(self):
		IASL_CMD_STR = "subprocess.call(['iasl', '-d', '%s'], stdout=subprocess.PIPE)"
		CAPABILITY_OFFSET = "0x08"
		CAP_REG_BYTE_SIZE = 7
		AGAW_BIT_START = 8
		IOMMU_SIZE = "1000"

		elemlist = []
		outputpath = paths.TEMP
		tempname = "dmar.dat"
		parsedname = tempname.split('.')[0] + ".dsl"

		print "> Parsing DMAR table with iasl tool..."
		dmarparser = parseutil.DMARParser()
		#Create parsed copy of DMAR table
		if dmarparser.genDMAR(paths.DMAR,
						outputpath,
						tempname):
			iaslcmdstr = IASL_CMD_STR % os.path.join(outputpath,tempname)
			if dmarparser.parseDMAR(iaslcmdstr):
				print "Parsing of DMAR file with iasl successful."
				#Get iommu addresses from DMAR
				iommuaddrs = dmarparser.getIommuAddrs(os.path.join(outputpath,
																  parsedname) )
				#Instantiate IommuNamer to set names for iommu devices
				iommunamer = self.IommuNamer(iommuaddrs)

				#Create Iommu devices
				for addr in iommuaddrs:
					elemlist.append(self.createDeviceFromAddr(paths.DEVMEM,
															  addr,
															  iommunamer,
															  IOMMU_SIZE,
															  CAPABILITY_OFFSET,
															  CAP_REG_BYTE_SIZE,
															  AGAW_BIT_START
															  )
								   )

		return elemlist
	"""

    def getIommuAGAW(self, iommuaddr, devmem, capoffset, capbytesize, agawbitstart):
        "Gets the AGAW name from a given iommuaddr, at the capability offset"
        AGAW_39_BITNO = 1
        AGAW_48_BITNO = 2
        AGAW_39_NAME = "39"
        AGAW_48_NAME = "48"

        name = "agaw"
        try:
            startaddr = int(iommuaddr, 16) + int(capoffset, 16)
            capreg = extractor.extractBinaryData(devmem,
                                                 startaddr,
                                                 capbytesize)
        except IOError:
            message.addError("Could not access file: %s" % devmem, False)
        else:
            agaw = (int(capreg, 16) >> agawbitstart) & 0x1F  # See 5 bits
            if util.getBit(agaw, AGAW_39_BITNO):
                name = AGAW_39_NAME
            elif util.getBit(agaw, AGAW_48_BITNO):
                name = AGAW_48_NAME
            else:
                message.addError("AGAW Capability could not be found for IOMMU "
                                 "device at: %s" % iommuaddr, False)
        return name

    def createDeviceFromAddr(self,
                             devmem,
                             iommuaddr,
                             iommunamer,
                             iommusize,
                             capoffset,
                             capregbytesize,
                             agaw_bit_start):
        "Generates a device element from a given iommu address"

        device = Element("device", "deviceType")
        device["shared"] = "false"

        # name attr
        device["name"] = iommunamer.getName()

        # memory
        memory = Element("memory", "deviceMemoryType")
        memory["caching"] = "UC"  # TODO
        memory["name"] = "mmio"
        memory["physicalAddress"] = util.toWord64(iommuaddr)
        memory["size"] = util.toWord64(iommusize)
        device.appendChild(memory)

        # capabilities
        capabilities = Element("capabilities", "capabilitiesType")
        # iommu
        iommucap = Element("capability", "capabilityType")
        iommucap["name"] = "iommu"
        capabilities.appendChild(iommucap)
        # agaw
        agawcap = Element("capability", "capabilityType")
        agawcap["name"] = "agaw"
        agawcap.content = self.getIommuAGAW(iommuaddr,
                                            devmem,
                                            capoffset,
                                            capregbytesize,
                                            agaw_bit_start)
        capabilities.appendChild(agawcap)
        device.appendChild(capabilities)

        return device


def createElements():
    "Creates the element tree and returns top element"
    platform = Element("platform", "platformType")
    platform.appendChild(ProcessorCreator().createElem(paths.CPUINFO, paths.MSR))
    platform.appendChild(MemoryCreator().createElem(paths.MEMMAP))
    platform.appendChild(DevicesCreator().createElem())

    return platform
