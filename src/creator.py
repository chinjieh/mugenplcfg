#Module that handles creation of the XML document
import parseutil
from schemadata import Element
import customExceptions
import util
import paths
import os
import message
import devicecap
import extractor
from collections import namedtuple

Address = namedtuple("Address", "start end")

class ProcessorCreator():

	@staticmethod
	def createElem():
		print "Creating element: processor"
		cpuinfo = extractor.extractData(paths.CPUINFO)
		processor = Element("processor", "processorType")
		processor["logicalCpus"] = parseutil.count(cpuinfo,"processor")
		processor["speed"] = float(parseutil.parseData_Sep(cpuinfo, "cpu MHz", ":"))
		processor["vmxTimerRate"] = ProcessorCreator.getVmxTimerRate()
		print "Element created: processor"
		return processor

	@staticmethod
	def getVmxTimerRate():
		#check for MSR	
		vmxTimerRate = 0	
		MSRfound = False
		OFFSET = 0x485
		VMX_BITS_START = 0
		VMX_BITS_END = 4
		for path in paths.MSR:
			try:
				#Try to find MSR file
				byte = extractor.extractBinaryData(path, OFFSET, 1)[0]
			except IOError:
				continue
			else:
				MSRfound = True
				break

		if MSRfound is False:
			errormsg = "MSR could not be located at directories:\n"
			for path in paths.MSR:
				errormsg += ("%s\n" % path)

			errormsg += "vmxTimerRate could not be found. Please add it manually, or try 'modprobe msr' to probe for MSR, then run the tool again.\n" + \
			"Alternatively, run the tool again with the proper permissions."
			message.addError(errormsg)
		else:
			vmxbits = 0
			#Get bits from VMX_BITS_START to VMX_BITS_END
			for bitnum in range(VMX_BITS_START, VMX_BITS_END+1):
				vmxbits += util.getBit(int(byte, 16), bitnum) << bitnum
			vmxTimerRate = int(vmxbits)

		return vmxTimerRate
	
class MemoryCreator():
	
	@staticmethod
	def createElem():
		print "Creating element: memory"

		memory = Element("memory", "physicalMemoryType")	
		#Get list of memoryBlocks available
		memoryBlockList = MemoryCreator.getMemoryBlocks(paths.MEMMAP)

		for memoryBlock in memoryBlockList:
			memory.appendChild(memoryBlock)
		print "Element created: memory"
		return memory
	
	@staticmethod
	def getMemoryBlocks(path):
		memoryBlockList = []
		for root,subdirs,files in os.walk(path):
			if not subdirs:  #at end of paths

				endfile = root + "/" + "end"
				typefile = root + "/" + "type"
				startfile = root + "/" + "start"
				try:
					memoryBlock = MemoryCreator.generateMemoryBlock(endfile,typefile,startfile)
				except IOError:
					message.addError("Could not retrieve complete memory data")
				#Adds newly created memoryBlock element to memoryBlockList			
				memoryBlockList.append(memoryBlock)

		return memoryBlockList

	@staticmethod
	def generateMemoryBlock(endfile,typefile,startfile):
		memoryBlock = Element("memoryBlock", "memoryBlockType")
		
		memoryBlock["name"] = extractor.extractData(typefile)
		if MemoryCreator.isAllocatable(memoryBlock["name"]):
			memoryBlock["allocatable"] = "true"
		else:
			memoryBlock["allocatable"] = "false"
	
		memoryBlock["physicalAddress"] = util.toWord64(extractor.extractData(startfile))
		memoryBlock["size"] = util.toWord64(util.sizeOf(extractor.extractData(endfile), extractor.extractData(startfile)) )
	
		return memoryBlock

	
	
	@staticmethod
	def isAllocatable(name):
		if name == "System RAM":
			return True
		else: 
			return False

class DevicesCreator():

	@staticmethod
	def createElem():
		print "Creating element: devices"
		devices = Element("devices", "devicesType")
		devices["pciConfigAddress"] = util.toWord64(DevicesCreator.getPciConfigAddress(paths.IOMEM))
		
		#Add Pci Devices
		devices.appendChild(PciDevicesCreator().createElems())

		#Add Tty Devices
		devices.appendChild(TtyDevicesCreator().createElems())

		print "Element created: devices"
	
		return devices

	@staticmethod
	def getPciConfigAddress(path):
		pciconfigaddr = ""
		key = "PCI MMCONFIG"
		try:
			iomemdata = extractor.extractData(path)
			keyline = parseutil.findLines(iomemdata, key)[0]
			pciconfigaddr = keyline.split("-")[0]
		
		except (customExceptions.KeyNotFound, IOError):
			message.addError("Could not obtain pciConfigAddress from %s." % path)

		return pciconfigaddr


class PciDevicesCreator():
	"Helper function of DevicesCreator"
	def __init__(self):	
		self.devicepaths = []
		self.capabilities = {} #devicepath = capabilitylist
		self.devicenames = {} #devicepath = name
		self.deviceShortNames = {} #devicepath = shortname

	def createElems(self):
		pcidevicelist = []
		print "Finding PCI devices..."
		self.devicepaths = self.findDevicePaths(paths.DEVICES)
		print "Checking Dependencies..."
		self.getDependencies()
		print "Examining PCI devices..."
		filteredpaths = self.filterDevicePaths(self.devicepaths)
		print "Extracting device information from %d PCI devices (excluding PCI bridges and non PCI-Express devices)..." % len(filteredpaths)
		for devicepath in filteredpaths:	
			device = self.createDeviceFromPath(devicepath)
			pcidevicelist.append(device)

		return pcidevicelist
	
	def getDependencies(self):
		"Checks whether dependencies are fulfilled and fills up the class attributes"
		self.capabilities = self.getCapabilities(self.devicepaths)
		#self.devicenames = self.getDeviceNames(self.devicepaths)
		self.deviceShortNames = self.getDeviceShortNames(self.devicepaths)

	def findDevicePaths(self, path):
		"Gets paths to all PCI devices in system"
		devicePaths = []
		devicePaths = util.getLinks(path, self.isDeviceName)
		return devicePaths
	
	def filterDevicePaths(self, devicePaths):
		"Returns filtered list of paths of devices"
		bridgePaths = []
		pciExpressPaths = []
		bridgedDevicePaths = []
		nonPciExpressPaths = []
		resultPaths = []
		for devicepath in devicePaths:
			if self.isPciExpress(devicepath):
				pciExpressPaths.append(devicepath)

			if self.isBridge(devicepath):
				bridgePaths.append(devicepath)
				for root, subdirs, files in os.walk(devicepath):
					for subdir in subdirs:
						if self.isDeviceName(subdir):
							bridgedDevicePaths.append(os.path.join(root,subdir))
		
		for bridgedDevice in bridgedDevicePaths:
			if self.isPciExpress(bridgedDevice) is False:
				nonPciExpressPaths.append(bridgedDevice)

		print "Devices found: %d\n------------------" % len(self.devicepaths)
		print "> PCI Bridges: ", len(bridgePaths)
		for item in bridgePaths:
			print "  ", os.path.basename(item)

		print "> Bridged Devices: ", len(bridgedDevicePaths)
		for item in bridgedDevicePaths:
			print "  ", os.path.basename(item)
					
		print "> PCI Express Devices: ", len(pciExpressPaths)
		for item in pciExpressPaths:
			print "  ", os.path.basename(item)

		resultPaths = util.removeListsFromList(devicePaths, bridgePaths, nonPciExpressPaths)
		return resultPaths

	def isBridge(self, devicepath):
		isBridge = False
		PCI_BRIDGE = "0x0604"
		if extractor.extractData(os.path.join(devicepath, "class"))[0:6] == PCI_BRIDGE:
			isBridge = True

		return isBridge

	def isPciExpress(self, devicepath):
		isPciExpress = False
		PCI_EXPRESS = "0x10"
		
		if PCI_EXPRESS in self.capabilities[devicepath]:
			isPciExpress = True
		
		return isPciExpress

	def isDeviceName(self, value):
		"Checks for format: ####:##[#]:##[#].#[#]"
		splitcolon = value.split(':')
		if len(splitcolon) != 3:
			return False
	
		if '.' not in splitcolon[2]:
			return False

		if len(splitcolon[0]) != 4:
			return False

		return True

	def getDeviceBus(self, devicestr):
		return devicestr.split(':')[1]

	def getDeviceNo(self, devicestr):
		return (devicestr.split(':')[2] ).split('.')[0]

	def getDeviceFunction(self, devicestr):
		return (devicestr.split(':')[2] ).split('.')[1]	

	def getCapabilities(self, devicepaths):	
		"Checks if device capabilities can be found"
		capabilities = {}

		#Initialise empty dictionary
		for devicepath in devicepaths:
			capabilities[devicepath] = []

		#Attempt to fill dictionary	
		try:
			for devicepath in devicepaths:
				capabilities[devicepath] = devicecap.getCapability(devicepath)
		except customExceptions.NoAccessToFile:
			message.addError("Not enough permissions to access capabilities of devices. " +
			"It is advised to run the tool again with the proper permissions.")		

		return capabilities

	#TODO Unused for now, while device names are relying on class codes and not Vendor and Device pairs
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
			pciIdsParser = parseutil.PciIdsParser(paths.PCIIDS + "pci.ids")

		except customExceptions.PciIdsFileNotFound:
			message.addError("pci.ids file could not be located in tool directory: %s. Device names could not be obtained.\n" % paths.CURRENTDIR +
			"Please ensure that the file is in the directory." )
		
		else:
			for devicepath in devicepaths:
				try:
					venhex = extractor.extractData(os.path.join(devicepath,"vendor") )
					devhex = extractor.extractData(os.path.join(devicepath,"device") ) 
					names[devicepath] = pciIdsParser.getVendorName(venhex) #TODO Name constraint
				except customExceptions.PciIdsFailedSearch as e:
					message.addWarning("Names for Device %s of Vendor %s could not be found. It would be a good idea to update pci.ids")			

				except customExceptions.PciIdsMultipleEntries as e:
					message.addWarning("Multiple names for Device %s of Vendor %s were found. Please insert the correct names manually in the XML " +
					"file.")

		return names
	"""

	def getDeviceShortNames(self, devicepaths):
		shortnames = {}
		namecount = {}
		#Initialise PciIdsParser
		try:
			pciIdsParser = parseutil.PciIdsParser(paths.PCIIDS + "pci.ids")
		
		except customExceptions.PciIdsFileNotFound:
			message.addError("pci.ids file could not be located in tool directory: %s. Device names could not be obtained.\n" % paths.CURRENTDIR +
			"Please ensure that the file is in the directory." )
		
		else:
			for devicepath in devicepaths:
				#Get class code from "class" file"
				classcode = extractor.extractData(os.path.join(devicepath, "class"))[0:6]
				classname = classcode
				try:
					classname = pciIdsParser.getClassName(classcode)
				
				except (customExceptions.PciIdsFailedSearch,
					customExceptions.PciIdsSubclassNotFound):
					message.addWarning(("Name for Device at: %s" % devicepath +
							" cannot be found. It would " + 
							"be a good idea to update pci.ids")
							)

				classname = util.spacesToUnderscores(classname.lower())

				#Add class name to namecount
				if classname not in namecount:
					namecount[classname] = 1
				else:
					namecount[classname] += 1

				#Add entry to dictionary
				shortnames[devicepath] = classname

		
		#Find repeated class names
		repeatednames = []
		shortnamesno = shortnames.copy()
		for item in namecount.items():
			if item[1] > 1:
				if item[0] not in repeatednames:
					repeatednames.append(item[0])

		#Append numbers to repeated names
		for repeatedname in repeatednames:
			counter = 1
			for dev in devicepaths:
				if shortnames[dev] == repeatedname:
					shortnamesno[dev] = "%s_%d" % (shortnames[dev], counter)
					counter += 1

		return shortnamesno

	def createDeviceFromPath(self, devicepath):
		pcistr = os.path.basename(devicepath)
		device = Element("device", "deviceType")
		#Old code that gets device name as Vendor DeviceName
		#device["name"] = self.devicenames[devicepath]
		device["name"] = self.deviceShortNames[devicepath]
		device["shared"] = "false" #TODO Check for shared status sometime in the future

		#pci
		pci = Element("pci", "pciType")
		pci["bus", "device", "function"] = util.wrap16(self.getDeviceBus(pcistr)), util.wrap16(self.getDeviceNo(pcistr)), self.getDeviceFunction(pcistr)
		device.appendChild(pci)
		
		#irq
		try:
			irqNo = extractor.extractData(os.path.join(devicepath,"irq"))
			if irqNo is not "0":
				irq = Element("irq", "irqType")
				irq["name", "number"] = "irq", irqNo
				device.appendChild(irq)

		except IOError:
			message.addError("Could not obtain irq number for device: %s" % pcistr)
		
		#memory, includes expansion roms
		try:
			resourceData = extractor.extractData(os.path.join(devicepath, "resource"))
			memcount = 0
			for line in resourceData.splitlines():
				tokens = line.split(' ')
				if tokens[2][-3] == '2': #if line represents a memory block
				
					memory = Element("memory", "deviceMemoryType")
					memory["name"] = "mem%d" % memcount
					memory["physicalAddress"] = util.toWord64(tokens[0])
					memory["size"] = util.toWord64(util.sizeOf(tokens[1], tokens[0]))
					memory["caching"] = "UC" #TODO
					memcount += 1
					device.appendChild(memory)
		
		except IOError:
			message.addError("Could not obtain memory information for device: %s" % pcistr)

		#ioports
		try:
			resourceData = extractor.extractData(os.path.join(devicepath, "resource"))
			ioportcount = 0
			for line in resourceData.splitlines():
				tokens = line.split(' ')
				if tokens[2][-3] == '1': #if line represents ioport information
				
					ioPort = Element("ioPort", "ioPortType")
					ioPort["name"] = "ioport%d" % ioportcount
					ioPort["start"] = util.toWord64(tokens[0])
					ioPort["end"] = util.toWord64(tokens[1])
					ioportcount += 1
					device.appendChild(ioPort)

		except IOError:
			message.addError("Could not obtain ioport information for device: %s" % pcistr)
	
		#capabilities	
		caplist = self.capabilities[devicepath]
		if caplist:
			capabilities = Element("capabilities", "capabilitiesType")
			for cap in caplist:
				capability = Element("capability", "capabilityType")
				capability["name"] = cap

				try:
					capability.setContent(devicecap.translate(cap))
				except customExceptions.CapabilityUnknown:
					message.addWarning("Capability code: %s is unknown. It might be a good idea to update 'devicecap.py'." % cap)
					capability.setContent(cap)

				capabilities.appendChild(capability)

			device.appendChild(capabilities)

		return device

class TtyDevicesCreator():
	"Helper function of DevicesCreator"

	def __init__(self):
		self.addresses = []
		self.ComAddresses = {
					Address("03f8", "03ff") : "com_1",
					Address("02f8", "02ff") : "com_2",
					Address("03e8", "03ef") : "com_3",
					Address("02e8", "02ef") : "com_4"
							} #TODO Check

	def createElems(self):
		ttydevicelist = []
		self.addresses = self.getSerialAddresses()
		#Get COM Device addresses
		for comdevice in self.createComDevices(self.ComAddresses):
			ttydevicelist.append(comdevice)
		#Filter COM devices from list
		filteredlist = util.removeListsFromList(self.addresses, self.ComAddresses.iterkeys())
		for serialdevice in self.createSerialDevices(filteredlist):
			ttydevicelist.append(serialdevice)
		return ttydevicelist

	def getSerialAddresses(self):
		"Gets serial addresses in form (startaddr, endaddr)"
		serialAddresses = []
		KEYWORD = "serial"

		#Get all lines which include KEYWORD
		try:
			ioportdata = extractor.extractData(paths.TTY)
		except IOError:
			message.addError("Could not access %s." % paths.TTY)
		else:
			lines = parseutil.findLines(ioportdata, KEYWORD)
			#Retrieve (start,end) data for serial devices		
			for line in lines:
				serialAddresses.append(self.getAddressFromLine(line))
		
		return serialAddresses

	def getAddressFromLine(self, line):
		"Parses line to obtain (start,end)"
		addrInfo = line.partition(":")[0].strip()
		start = addrInfo.partition("-")[0]
		end = addrInfo.partition("-")[2]
		addr = Address(start, end)
		return addr

	def createComDevices(self,comAddresses):
		comdevices = []
		for addr in self.ComAddresses:
		    	device = Element("device", "deviceType")
		    	device["name"] = "test"
			device["shared"] = "true"
			ioport = Element("ioport", "ioPortType")
			ioport["name"] = "port"
			ioport["start"] = util.toWord64(addr.start)
			ioport["end"] = util.toWord64(addr.end)
			device.appendChild(ioport)
			comdevices.append(device)
		return comdevices

	def createSerialDevices(self,addresses):
		devices = []
		device = Element("device", "deviceType")
		device["name"] = "name"
		device["shared"] = "true"
		devices.append(device)
		#TODO
		return devices

def createElements():
	"Creates the element tree and returns top element"
	platform = Element("platform", "platformType")
	platform.appendChild(ProcessorCreator.createElem())	
	platform.appendChild(MemoryCreator.createElem())
	platform.appendChild(DevicesCreator.createElem())

	return platform	

