#Module that runs test cases with PyUnit
import sys; sys.dont_write_bytecode = True
import unittest
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import testpaths
from src import schemadata, customExceptions
from collections import namedtuple
# == Class that tests extractor.py ==
import src.extractor as extractor
class ExtractorTestCase(unittest.TestCase):

	"Tests the extractor file"
	def setUp(self):
		"Setup code"
		print "<> ExtractorTestCase:setUp - begin"
		self.testdir = testpaths.PATH_TEST_EXTRACTOR

	def tearDown(self):
		"Cleanup code"
		print "<> ExtractorTestCase:tearDown - begin"

	## -- extractData testcases
	def test_extractData(self):
		"Tests the extractData function"
		print "ExtractorTestCase:test_extractData - begin"

		loc = self.testdir + "testExtractData.txt"
		self.assertEqual(extractor.extractData(loc), "test", "Extracted Data from file "+ loc +" does not match.")
		self.assertNotEqual(extractor.extractData(loc), "test2", "Extracted Data from file "+ loc +" matches incorrectly.")
		self.assertNotEqual(extractor.extractData(loc), "", "Extracted Data from file "+ loc +" matches incorrectly.")

	def test_extractData_blank(self):
		"Tests the extractData function with blank file"
		print "ExtractorTestCase:test_extractData_blank - begin"

		loc = self.testdir + "testExtractData_blank.txt"
		self.assertEqual(extractor.extractData(loc), "", "Extracted Data from file "+ loc +" does not match.")

	def test_extractData_doesNotExist(self):
		"Tests the extractData function with file that does not exist"
		print "ExtractorTestCase:test_extractData_doesNotExist - begin"

		loc = self.testdir + "testExtractData_shouldnotexist.txt"
		self.assertRaises(IOError,extractor.extractData,loc)

	## -- extractBinaryData testcases
	def test_extractBinaryData(self):
		"Tests the extractBinaryData function"
		print "ExtractorTestCase:test_extractBinaryData - begin"
		loc = self.testdir + "testExtractBinaryData"
		with open(loc, "wb") as f:
			f.write(b"\x01\x02\x03\x04")
		self.assertEqual(extractor.extractBinaryData(loc, 0, 4), "0x04030201", "extractBinaryData function not working")
		self.assertEqual(extractor.extractBinaryData(loc, 0, 4, chunks=True), ["0x04","0x03","0x02","0x01"], "extractBinaryData function not working")
		self.assertEqual(extractor.extractBinaryData(loc, 2, 2, chunks=True), ["0x04","0x03"], "extractBinaryData function not working")
		self.assertEqual(extractor.extractBinaryData(loc, 0, 2, "LITTLE_ENDIAN", chunks=True), ["0x01", "0x02"], "extractBinaryData function not working")
		self.assertRaises(customExceptions.NoAccessToFile, extractor.extractBinaryData, loc, 3, 2)

# == Class that tests creator.py ==
import src.creator as creator
class CreatorTestCase(unittest.TestCase):
	"Tests the creator.py file"

	def setUp(self):
		print "<> CreatorTestCase:setUp - begin"
		self.testdir = testpaths.PATH_TEST_CREATOR

	def tearDown(self):
		print "<> CreatorTestCase:tearDown - begin"

	## -- DevicesCreator testcases
	def test_DevicesCreator(self):
		"Tests the DevicesCreator class"
		print "CreatorTestCase:test_DevicesCreator - begin"

		#Test getPciConfigAddress function
		testiomem = os.path.join(self.testdir,"devicescreator/test_iomem")
		testinvalidloc = os.path.join(self.testdir,"devicescreator")
		testnokey = os.path.join(self.testdir,"devicescreator/test_iomem_nopciconfig")
		self.assertEqual(creator.DevicesCreator.getPciConfigAddress(testiomem), "e0000000", "getPciConfigAddress function not working")
		creator.DevicesCreator.getPciConfigAddress(testinvalidloc)
		creator.DevicesCreator.getPciConfigAddress(testnokey)

	## -- PciDevicesCreator testcases
	def test_PciDevicesCreator(self):
		"Tests the PciDevicesCreator class"
		pcicreator = creator.PciDevicesCreator()
		devloc = os.path.join(self.testdir, "devicescreator/devices")

		#Test isDeviceName function
		self.assertEqual(pcicreator.isDeviceName("0000:01:00.0"), True, "isDeviceName function not working")
		self.assertEqual(pcicreator.isDeviceName("0000:00:01.2"), True, "isDeviceName function not working")
		self.assertEqual(pcicreator.isDeviceName("0001:17:02.5"), True, "isDeviceName function not working")
		self.assertEqual(pcicreator.isDeviceName("010:10:01.2"), False, "isDeviceName function not working")
		self.assertEqual(pcicreator.isDeviceName("0000:10:01"), False, "isDeviceName function not working")
		self.assertEqual(pcicreator.isDeviceName("000:10:01.1"), False, "isDeviceName function not working")
		self.assertEqual(pcicreator.isDeviceName("0003:0E0F:0003.0001"), False, "isDeviceName function not working")
		
		#Test isBridge function
		self.assertEqual(pcicreator.isBridge(os.path.join(devloc, "pcibridge0")), True, "isBridge function not working")
		self.assertEqual(pcicreator.isBridge(os.path.join(devloc, "dev0")), False, "isBridge function not working")

		#Test getDeviceBus function
		self.assertEqual(pcicreator.getDeviceBus("0011:01:02.3"), "01", "getDeviceBus function not working")

		#Test getDeviceNo function
		self.assertEqual(pcicreator.getDeviceNo("0000:01:02.3"), "02", "getDeviceNo function not working")

		#Test getDeviceFunction function
		self.assertEqual(pcicreator.getDeviceFunction("0000:01:02.3"), "3", "getDeviceFunction function not working")

	## -- SerialDevicesCreator testcases
	def test_SerialDevicesCreator(self):
		"Tests the SerialDevicesCreator class"
		serialcreator = creator.SerialDevicesCreator()

		#Test getAddressFromLine function
		self.assertEqual(serialcreator.getAddressFromLine("  3e0f-3e50 : serial"), ("3e0f", "3e50"), "getAddressFromLine function not working")
		self.assertEqual(serialcreator.getAddressFromLine("    3e05-3e10 : serial"), ("3e05", "3e10"), "getAddressFromLine function not working")

	## -- IommuDevicesCreator testcases
	def test_IommuDevicesCreator(self):
		"Tests the IommuDevicesCreator class"
		iommucreator = creator.IommuDevicesCreator()

		#Test getIommuAddrs function
		loc = os.path.join(self.testdir, "devicescreator/testdmar.dsl")
		emptyloc = os.path.join(self.testdir, "devicescreator/testdmar_empty.dsl")

		self.assertEqual(iommucreator.getIommuAddrs(loc),
				["0xfed91000", "0xfed91100"],
				"getIommuAddrs function not working")
		self.assertEqual(iommucreator.getIommuAddrs(emptyloc),
				[],
				"getIommuAddrs function not working")
		
	## -- ProcessorCreator testcases
	def test_ProcessorCreator(self):
		"Tests the ProcessorCreator class"
		print "CreatorTestCase:test_ProcessorCreator - begin"
		
		#Test getSpeed function
		speedkeywords = ["GHz","MHz"]
		testline = """model name	: Intel(R) Xeon(R) CPU E31230 @ 3.20GHz"""
		testline2 = """model name	: Intel(R) Xeon(R) CPU E31230 @ 800MHz"""
		testline3 = """model name	: Intel(R) Xeon(R) CPU E31230 @ 3.20GH"""
		testline4 = """model name	: 3.20GHz Intel(R) Xeon(R) CPU E31230"""
		testline5 = """model name	: 3.20 GHz Intel(R) Xeon(R) CPU"""
		self.assertEqual(creator.ProcessorCreator.getSpeed(testline, speedkeywords), "3200", "getSpeed function not working")
		self.assertEqual(creator.ProcessorCreator.getSpeed(testline2, speedkeywords), "800", "getSpeed function not working")
		self.assertRaises(customExceptions.ProcessorSpeedNotFound,creator.ProcessorCreator.getSpeed,testline3, speedkeywords)
		self.assertEqual(creator.ProcessorCreator.getSpeed(testline4, speedkeywords), "3200", "getSpeed function not working")
		self.assertRaises(customExceptions.ProcessorSpeedNotFound,creator.ProcessorCreator.getSpeed,testline5, speedkeywords)
		
		#Test getVmxFromMSR function
		msrpath = os.path.join(testpaths.PATH_TEST_CREATOR, "testmsr")
		with open(msrpath, "wb") as f:
			f.write(b"\x01\x02\x03\x04")
		OFFSET = 0
		VMX_BITSIZE = 5
		self.assertEqual(creator.ProcessorCreator.getVmxFromMSR(msrpath, OFFSET, VMX_BITSIZE), 1, "getVmxFromMSR function not working")
		with open(msrpath, "wb") as f:
			f.write(b"\x05\x02\x03\x04")
		self.assertEqual(creator.ProcessorCreator.getVmxFromMSR(msrpath, OFFSET, VMX_BITSIZE), 5, "getVmxFromMSR function not working")
		with open(msrpath, "wb") as f:
			f.write(b"\x11\x02\x03\x04")
		self.assertEqual(creator.ProcessorCreator.getVmxFromMSR(msrpath, OFFSET, VMX_BITSIZE), 17, "getVmxFromMSR function not working")
		msrinvalidpath = os.path.join(testpaths.PATH_TEST_CREATOR, "testmsr_invalid")
		self.assertRaises(customExceptions.MSRFileNotFound, creator.ProcessorCreator.getVmxFromMSR, msrinvalidpath, OFFSET, VMX_BITSIZE)
				
		

	## -- MemoryCreator testcases
	def test_MemoryCreator(self):
		"Tests the MemoryCreator class"
		print "ExtractorTestCase:test_MemoryCreator - begin"

		loc = self.testdir + "memorycreator/"

		#Test isAllocatable function
		memblock_1 = Element("memoryBlock", "memoryBlockType")
		memblock_1["name", "physicalAddress"] = "System RAM", "16#0010_000f#"
		
		memblock_2 = Element("memoryBlock", "memoryBlockType")
		memblock_2["name", "physicalAddress"] = "System RAM2", "16#0010_000f"
		
		memblock_3 = Element("memoryBlock", "memoryBlockType")
		memblock_3["name", "physicalAddress"] = "System RAM", "0xfffff"
		
		memblock_4 = Element("memoryBlock", "memoryBlockType")
		memblock_4["name", "physicalAddress"] = "System RAM2", "0x1000"
		self.assertEqual(creator.MemoryCreator.isAllocatable(memblock_1),True, "isAllocatable function is not working")
		self.assertEqual(creator.MemoryCreator.isAllocatable(memblock_2), False, "isAllocatable function is not working")
		self.assertEqual(creator.MemoryCreator.isAllocatable(memblock_3),False,"isAllocatable function is not working")
		self.assertEqual(creator.MemoryCreator.isAllocatable(memblock_4), False, "isAllocatable function is not working")

		#Test getMemoryBlocks
		memoryBlockList = creator.MemoryCreator.getMemoryBlocks(loc)
		memoryBlock0 = memoryBlockList[0].compileToPyxb()
		memoryBlock1 = memoryBlockList[1].compileToPyxb()
		self.assertEqual(memoryBlock0.physicalAddress,"16#000a#", "getMemoryBlocks function not working")
		self.assertEqual(memoryBlock0.size,"16#f000#", "getMemoryBlocks function not working")
		self.assertEqual(memoryBlock1.name,"1_type", "getMemoryBlocks function not working")

		#Test generateMemoryBlock
		startfile = loc + "0/start"
		endfile = loc + "0/end"
		typefile = loc + "0/type"

		memoryBlock = creator.MemoryCreator.generateMemoryBlock(endfile, typefile, startfile)
		memoryBlock_pyxb = memoryBlock.compileToPyxb()
		self.assertEqual(memoryBlock_pyxb.name, "0_type", "generateMemoryBlock not working")
		self.assertEqual(memoryBlock_pyxb.physicalAddress, "16#000a#", "generateMemoryBlock not working")


# == Tests schemadata.py ==
from src.schemadata import Element
import schemadata.testschema as schema
import copy

class SchemaDataTestCase(unittest.TestCase):
	"Tests the schemadata file"

	def setUp(self):
		print "<> SchemaDataTestCase:setUp - begin"

	def tearDown(self):
		print "<> SchemaDataTestCase:tearDown - begin"


	## - Element class testcases
	def test_Element_toXML(self):
		"Tests the toXML function"
		print "SchemaDataTestCase:test_Element_toXML - begin"

		processor = Element("processor", "processorType")
		processor["logicalCpus", "speed", "vmxTimerRate"] = 1, 2, 3

		testxml = """<?xml version="1.0" encoding="utf-8"?><processor logicalCpus="1" speed="2" vmxTimerRate="3"/>"""
		self.assertEqual(processor.toXML("utf-8"), testxml, "toXML function not working")

	def test_Element_SetAttribute(self):
		"Tests the validity of setting attributes"
		print "SchemaDataTestCase:test_Element_SetAttribute - begin"

		processor = Element("processor", "processorType")
		processor["logicalCpus"] = 10
		processor["speed"] = 15
		processor["vmxTimerRate"] = [20]

		#Test for setting of invalid attribute of processorType
		self.assertRaises(customExceptions.InvalidAttribute, processor.__setitem__, "price", 100)

		#Test for permanence of attribute setting when converted to binding Pyxb object
		processor_pyxb = processor.compileToPyxb()
		self.assertEqual(processor_pyxb.logicalCpus, 10, "Attribute setting failed")
		self.assertEqual(processor_pyxb.speed, 15, "Attribute setting failed")
		
		#Test for correctly not setting empty attributes
		devices = Element("devices", "devicesType")
		devices["pciConfigAddress"] = ""
		devices.compileToPyxb()

		#Test for setting multiple attributes
		processor["logicalCpus", "speed", "vmxTimerRate"] = 1, 2, 3
		processor_pyxb = processor.compileToPyxb()
		self.assertEqual(processor_pyxb.logicalCpus, 1, "Multiple attribute setting failed")
		self.assertEqual(processor_pyxb.speed, 2, "Multiple attribute setting failed")
		self.assertEqual(processor_pyxb.vmxTimerRate, 3, "Multiple attribute setting failed")

		self.assertRaises(customExceptions.AttributeMismatch, processor.__setitem__, ["logicalCpus", "speed"], [1,2,3])
		self.assertRaises(customExceptions.InvalidAttribute, processor.__setitem__, ["logicalCpus", "price", "speed"], [1,2,3])

	def test_Element_SetContent(self):
		"Tests the validity of setting element content"
		print "SchemaDataTestCase:test_Element_SetContent - begin"
		capability = Element("capability", "capabilityType")
		capability.setContent("Content1")
		capability["name"] = "content1"
		testXML = """<?xml version="1.0" encoding="utf-8"?><capability name="content1">Content1</capability>"""
		self.assertEqual(capability.toXML('utf-8'), testXML, "setContent function not working")

	def test_Element_GetItem(self):
		"Tests the validity of retrieving attributes"
		print "SchemaDataTestCase:test_Element_GetItem - begin"

		processor = Element("processor", "processorType")
		processor["logicalCpus"] = 10
		processor["speed"] = 15
		processor["vmxTimerRate"] = [20]

		self.assertEqual(processor["logicalCpus"], 10, "Attribute Retrieving failed")
		self.assertRaises(customExceptions.InvalidAttribute, processor.__getitem__, "price")

	def test_Element_appendChild(self):
		"Tests the capability to add and remove child elements"
		print "SchemaDataTestCase:test_Element_appendChild - begin"

		memory = Element("memory", "physicalMemoryType")

		memoryBlock = Element("memoryBlock", "memoryBlockType")
		memoryBlock["physicalAddress", "size", "name"] = "16#1111#", "16#2222#", "mem"

		memoryBlock2 = Element("memoryBlock", "memoryBlockType")
		memoryBlock2["physicalAddress", "size", "name", "allocatable"] = "16#0101#", "16#0000#", "mem2", "true"

		memory.appendChild(memoryBlock)
		memory_pyxb = memory.compileToPyxb()
		self.assertEqual(memory_pyxb.memoryBlock[0].size, "16#2222#", "appendChild function failed")

		memory.removeChild(memoryBlock)
		memory_pyxb = memory.compileToPyxb()
		self.assertRaises(IndexError, memory_pyxb.memoryBlock.__getitem__, 0)

		memory.appendChild(memoryBlock, memoryBlock2)
		memory_pyxb = memory.compileToPyxb()
		self.assertEqual(memory_pyxb.memoryBlock[1].name, "mem2", "appendChild function failed")

	def test_Element_ListElements(self):
		"Tests the capabilities to include list elements"
		print "SchemaDataTestCase:test_Element_listElements - begin"

		memory = Element("memory", "physicalMemoryType")

		memoryBlock = Element("memoryBlock", "memoryBlockType")
		memoryBlock["physicalAddress", "size", "name"] = "16#0000#", "16#4fff#", "mem1"

		memoryBlock2 = Element("memoryBlock", "memoryBlockType")
		memoryBlock2["physicalAddress", "size", "name", "allocatable"] = "16#0101#", "16#0000#", "mem2", "true"

		memoryBlock3 = Element("memoryBlock2", "memoryBlockType")
		memoryBlock3["physicalAddress", "size", "name"] = "16#abcd#", "16#1234#", "mem3"

		memory.appendChild(memoryBlock)
		memory.appendChild(memoryBlock2)
		memory.appendChild(memoryBlock3)


		memory_pyxb = memory.compileToPyxb()
		self.assertEqual(memory_pyxb.memoryBlock[0].name, "mem1", "Nesting of list elements failed")
		self.assertEqual(memory_pyxb.memoryBlock[1].physicalAddress, "16#0101#", "Nesting of list elements failed")

		testXML = """<?xml version="1.0" encoding="utf-8"?><memory><memoryBlock name="mem1" physicalAddress="16#0000#" size="16#4fff#"/>"""
		testXML += """<memoryBlock allocatable="true" name="mem2" physicalAddress="16#0101#" size="16#0000#"/></memory>"""

		self.assertEqual(memory.toXML("utf-8"),testXML,"Compiling of list elements does not match expected output")


	def test_Element_NestedElements(self):
		"Tests the capabilities to have deep nested elements"
		print "SchemaDataTestCase:test_Element_NestedElements - begin"

		devices = Element("devices", "devicesType")
		devices["pciConfigAddress"] = "16#0000#"

		device1 = Element("device", "deviceType")
		device1["shared", "name"] = "true", "Device1"

		device1_pci = Element("pci", "pciType")
		device1_pci["bus", "device", "function"] = "16#4f#", "16#0a#", 4
		device1.appendChild(device1_pci)

		device1_ioPort1 = Element("ioPort", "ioPortType")
		device1_ioPort1["name", "start", "end"] = "device1_ioPort1", "16#0000#", "16#ffff#"
		device1_ioPort2 = Element("ioPort", "ioPortType")
		device1_ioPort2["name", "start", "end"] = "device1_ioPort2", "16#1111#", "16#aaaa#"

		device1.appendChild( device1_ioPort1, device1_ioPort2 )

		device1_capabilities = Element("capabilities", "capabilitiesType")
		device1.appendChild(device1_capabilities)
		device1_capabilitytype1 = Element("capability", "capabilityType")
		device1_capabilitytype1["name"] = "Device1 Capability1"
		device1_capabilitytype2 = Element("capability", "capabilityType")
		device1_capabilitytype2["name"] = "Device1 Capability2"
		device1_capabilities.appendChild( device1_capabilitytype1, device1_capabilitytype2 )

		device2 = Element("device", "deviceType")
		device2["shared", "name"] = "false", "Device2"

		device2_irq1 = Element("irq", "irqType")
		device2_irq1["name", "number"] = "device2_irq1", "100"
		device2_irq2 = Element("irq", "irqType")
		device2_irq2["name", "number"] = "device2_irq2", "200"
		device2.appendChild(device2_irq1, device2_irq2)
		device2_memory1 = Element("memory", "deviceMemoryType")
		device2_memory2 = Element("memory", "deviceMemoryType")
		device2.appendChild(device2_memory1,device2_memory2)
		device2_memory1["name","physicalAddress","size","caching"] = "device2_memory1","16#0000#","16#1111#","UC"
		device2_memory2["name", "physicalAddress","size","caching"] = "device2_memory2", "16#3333#", "16#4444#", "WC"


		devices.appendChild(device1,device2)
		devices_pyxb = devices.compileToPyxb()

		self.assertEqual(devices_pyxb.device[1].irq[1].name, "device2_irq2", "Deep nesting of elements failed")
		self.assertEqual(devices_pyxb.device[0].capabilities.capability[0].name, "Device1 Capability1", "Deep nesting of elements failed")
		self.assertEqual(devices_pyxb.device[1].shared, "false", "Deep nesting of elements failed")


# == Class that tests devicecap.py ==
import src.devicecap as devicecap
class DevicecapTestCase(unittest.TestCase):
	"Tests the devicecap file"
	def setUp(self):
		print "<> DevicecapTestCase:setUp - begin"
		self.testdir = testpaths.PATH_TEST_DEVICECAP

	def tearDown(self):
		print "<> DevicecapTestCase:tearDown - begin"

	def test_translate(self):
		"Tests the translate function"
		print "DevicecapTestCase:test_translate - begin"
		self.assertEqual(devicecap.translate("0x10"), "PCI Express", "translate function not working")
		self.assertRaises(customExceptions.CapabilityUnknown, devicecap.translate, "0x0101")
		
	def test_DevicecapManager(self):
		"Tests the DevicecapManager class"
		print "DevicecapTestCase:test_DevicecapManager - begin"
		devicecapmgr = devicecap.DevicecapManager()
		devloc = os.path.join(self.testdir,"devices")
		
		devpaths = [os.path.join(devloc,subdir) for subdir in os.listdir(devloc)]
		devicecapmgr.extractCapabilities(devpaths)
		devicecapmgr.getCapList(devpaths[0], False)
		devicecapmgr.getCapList(devpaths[1])
		devicecapmgr.getCapValue(devpaths[0], "0x09")
		devicecapmgr.getCapValue(devpaths[1], "0x09")
		
		# -- readCapFile function
		loc = os.path.join(self.testdir, "testReadCapFile")
		with open(loc, "wb") as f:
				   #00  01  02  03  04  05  06  07  08  09  0a  0b  0c  0d  0e  0f
			f.write(b"\x00\x01\x04\x03\x0a\x0e\x0c\x0a\x0e\x0c\x0d\x08\x0f\x00\x0b\x06")
		test_capcode1 = [cap.code for cap in devicecapmgr._readCapFile(loc,0x02,1,1)]
		test_capcode2 = [cap.code for cap in devicecapmgr._readCapFile(loc,0x02,1,1,0x0,3)]
		self.assertEqual(test_capcode1, ["0x0a", "0x0b", "0x0c", "0x0d", "0x0e", "0x0f"], "readCapFile function not working")
		self.assertEqual(test_capcode2, ["0x0a", "0x0b", "0x0c"], "readCapFile function not working")
		noaccessloc = os.path.join(devloc, "dev1_noaccess/config")
		# Read out of bounds offset to simulate "no access" - only 64 bytes
		# can be read without being root user
		self.assertRaises(customExceptions.NoAccessToFile,
						  devicecapmgr._readCapFile,
						  noaccessloc, os.stat(noaccessloc).st_size + 1, 1, 1)


# == Class that tests util.py ==
import src.util as util

class UtilTestCase(unittest.TestCase):
	"Tests the util file"

	def setUp(self):
		print "<> UtilTestCase:setUp - begin"

	def tearDown(self):
		print "<> UtilTestCase:tearDown - begin"

	def test_removeListsFromList(self):
		"Tests the removeListsFromList function"
		print "UtilTestCase:test_removeListsFromList - begin"
		mainList = [1,2,3,4,5,6,7,8,9,10]
		removeList1 = [2,4]
		removeList2 = [3,7]
		removeList3 = [3,6]
		removeList4 = [1,2,3,4,5,6,7,8,9,10]
		self.assertEqual(util.removeListsFromList(mainList, removeList1, removeList2), [1,5,6,8,9,10], "removeListsFromList function not working")
		self.assertEqual(util.removeListsFromList(mainList, removeList2, removeList3), [1,2,4,5,8,9,10], "removeListsFromList function not working")
		self.assertEqual(util.removeListsFromList(mainList, removeList4), [], "removeListsFromList function not working")

	def test_getBit(self):
		"Tests the getBit function"
		print "UtilTestCase:test_getBit - begin"
		self.assertEqual(util.getBit(5,2), 1, "getBit function not working")
		self.assertEqual(util.getBit(5,5), 0, "getBit function not working")

	def test_getLinks(self):
		"Tests the getLinks function"
		print "UtilTestCase:test_getLinks - begin"
		testdir = os.path.join(testpaths.PATH_TEST_UTIL, "test_getFilesInPath")

		def filterexp(filename):
			if filename.startswith("file"):
				return True
			else:
				return False

		testfilteredlist = ["file0", "file1", "file2", "file3"]

		#Get the absolute location of symbolic links in path
		testfilteredpaths = []
		for filename in testfilteredlist:
			filePath = os.path.join(testdir,filename)
			relativeLink = os.readlink(filePath)
			absLink = os.path.join(os.path.dirname(filePath), relativeLink)
			testfilteredpaths.append(absLink)

		self.assertEqual(util.getLinks(testdir,filterexp),
				testfilteredpaths,
				"getFilesInPath function not working")
		
	def test_getSpeedValue(self):
		"Tests the getSpeedValue function"
		print "UtilTestCaseL:test_getSpeedValue - begin"
		validspeeds = ["GHz", "MHz"]
		self.assertEqual(util.getSpeedValue("3.20GHz",validspeeds), "3200", "getSpeedValue function not working")
		self.assertEqual(util.getSpeedValue("800.0MHz",validspeeds),"800","getSpeedValue function not working")
		self.assertRaises(util.getSpeedValue("800KHz",validspeeds), None, "getSpeedValue function not working")
		self.assertEqual(util.getSpeedValue("0GHz",validspeeds),"0", "getSpeedValue function not working")

	def test_numberMultiples(self):
		"Tests the numberMultiples function"
		print "UtilTestCase:test_numberMultiples - begin"
		testlist = ["elem", "elem", "elem2", "elem2", "elem3"]
		resultlist = ["elem_1", "elem_2", "elem2_1", "elem2_2", "elem3"]
		failedlist = ["elem_1", "elem2_1", "elem_2", "elem2_2", "elem3"]
		self.assertEqual(util.numberMultiples(testlist), resultlist, "numberMultiples function not working")
		self.assertEqual(util.numberMultiples([]), [], "numberMultiples function not working")

	def test_ListNumberer(self):
		"Tests the ListNumberer class"
		print "UtilTestCase:test_ListNumberer - begin"
		testlist = ["elem", "elem", "elem2", "elem2", "elem3"]
		listnumberer = util.ListNumberer(testlist)
		self.assertEqual(listnumberer.getName("elem"), "elem_1", "ListNumberer class not working")
		self.assertEqual(listnumberer.getName("elem"), "elem_2", "ListNumberer class not working")
		self.assertEqual(listnumberer.getName("elem2"), "elem2_1", "ListNumberer class not working")
		self.assertEqual(listnumberer.getName("elem3"), "elem3", "ListNumberer class not working")
		self.assertRaises(ValueError, listnumberer.getName, "elem4")

	def test_isHex(self):
		"Tests the isHex function"
		print "UtilTestCase:test_isHex - begin"
		self.assertEqual(util.isHex("0x34Fa"), True, "isHex function not working")
		self.assertEqual(util.isHex("03Fa0x"), False, "isHex function not working")

	def test_stripvalue(self):
		"Tests the stripvalue function"
		print "UtilTestCase:test_stripvalue - begin"
		self.assertEqual(util.stripvalue("0x5123fa"), "5123fa", "stripvalue function not working")

	def test_toWord64(self):
		"Tests the toWord64 function"
		print "UtilTestCase: test_toWord64 - begin"
		self.assertEqual(util.toWord64("0x5faFFaD"), "16#05fa_FFaD#", "toWord64 function not working")
		self.assertEqual(util.toWord64("0x0"), "16#0000#", "toWord64 function not working")
		
	def test_unwrapWord64(self):
		"Tests the unwrapWord64 function"
		print "UtilTestCase: test_unwrapWord64 - begin"
		self.assertEqual(util.unwrapWord64("16#0009_a000#"), "0x9a000", "unwrapWord64 function not working")
		self.assertEqual(util.unwrapWord64("16#0000#"), "0x0", "unwrapWord64 function not working")
		self.assertEqual(util.unwrapWord64("0x1234"),"0x1234", "unwrapWord64 function not working")
		self.assertRaises(ValueError, util.unwrapWord64, "15#0009_a000#")

	def test_wrap16(self):
		"Tests the wrap16 function"
		print "UtilTestCase: test_wrap16 - begin"
		self.assertEqual(util.wrap16("1234"), "16#1234#", "wrap16 function not working")
		self.assertEqual(util.wrap16(""), "16##", "wrap16 function not working")

	def test_spacesToUnderscores(self):
		"Tests the spacesToUnderscores function"
		print "UtilTestCase: test_spacesToUnderscores - begin"
		self.assertEqual(util.spacesToUnderscores("asd def"), "asd_def", "spacestoUnderscores function not working")

	def test_sizeOf(self):
		"Tests the sizeOf function"
		print "UtilTestCase: test_sizeOf - begin"
		self.assertEqual(util.sizeOf("0x0002", "0x0001"), "0x2", "sizeOf function not working")
		self.assertEqual(util.sizeOf("0xe000", "0xe07f"), "0x80", "sizeOf function not working")
		self.assertRaises(ValueError, util.sizeOf, "0x1000", 2)

	def test_hexFloor(self):
		"Tests the hexFloor function"
		print "UtilTestCase: test_hexFloor - begin"
		MINSIZE = "0x1000"
		self.assertEqual(util.hexFloor("0x10",MINSIZE),MINSIZE, "hexFloor function not working")
		self.assertEqual(util.hexFloor("0x1000",MINSIZE), "0x1000", "hexFloor function not working")
		self.assertEqual(util.hexFloor("0x10000", MINSIZE), "0x10000", "hexFloor function not working")
		
	def test_hexRoundToMultiple(self):
		"Tests the hexRoundToMultiple function"
		print "UtilTestCase: test_hexRoundToMultiple - begin"
		self.assertEqual(util.hexRoundToMultiple("0x9d800","0x1000"), "0x9e000", "hexRoundToMultiple function not working")
		self.assertEqual(util.hexRoundToMultiple("0x9e000","0x1000"), "0x9e000", "hexRoundToMultiple function not working")
		self.assertEqual(util.hexRoundToMultiple("0x9d800","0x1000",rounddown=True),"0x9d000", "hexRoundToMultiple function not working")


# == Class that tests update.py ==
from src import update
import urllib2
class UpdateTestCase(unittest.TestCase):
	"Tests the update.py file"
	def setUp(self):
		"Setup code"
		print "<> UpdateTestCase:setUp - begin"
		self.testdir = testpaths.PATH_TEST_UPDATE

	def tearDown(self):
		"Cleanup code"
		print "UpdateTestCase:tearDown - begin"

	# -- updatePciIds tests
	def test_updatePciIds(self):
		"Tests updatePciIds function"
		INVALID_ADDR = "http://test"
		testfile = os.path.join(self.testdir,"test_pciids.ids")
		self.assertRaises(customExceptions.PciIdsInvalidLink,
						  update.updatePciIds,
						  INVALID_ADDR, testfile)


# == Class that tests parseutil.py ==
from src import parseutil
class ParseUtilTestCase(unittest.TestCase):
	"Tests the parseutil file"
	def setUp(self):
		"Setup code"
		print "<> ParseUtilTestCase:setUp - begin"
		self.testdir = testpaths.PATH_TEST_PARSEUTIL

	def tearDown(self):
		"Cleanup code"
		print "ParseUtilTestCase:tearDown - begin"

	# -- parseLine_Sep tests
	def test_parseLine_Sep(self):
		"Tests parseLine_Sep normal function"
		print "ParseUtilTestCase:test_parseLine_Sep - begin"

		loc = self.testdir + "testParseUtil.txt"
		data = extractor.extractData(loc)
		self.assertEqual(parseutil.parseLine_Sep(data.splitlines()[4], "testKey4", ":"), "testValue4", "Value obtained from file "+ loc +" is incorrect.")
		self.assertEqual(parseutil.parseLine_Sep(data.splitlines()[0], "testKey"), "testValue", "Value obtained from file "+ loc +" is incorrect.")
		self.assertEqual(parseutil.parseLine_Sep(data.splitlines()[0], "testKey", [":", ",", ""]), "testValue", "Value obtained from file "+ loc +"is incorrect.")

		loc = self.testdir + "testCpuInfo.txt"
		data = extractor.extractData(loc)
		self.assertEqual(parseutil.parseLine_Sep(data.splitlines()[8], "cache size", ":"), "8192 KB", "Value obtained from file "+ loc +" is incorrect.")
		self.assertEqual(
		parseutil.parseLine_Sep(data.splitlines()[4], "model name", ":"),
		"Intel(R) Xeon(R) CPU E31230 @ 3.20GHz",
		"Value obtained from file "+ loc +" is incorrect."
		)

	def test_parseLine_Sep_keyDoesNotExist(self):
		"Tests parseLine_Sep with nonexistent key"
		print "ParseUtilTestCase:test_parseLine_Sep_keyDoesNotExist - begin"

		loc = self.testdir + "testParseUtil.txt"
		data = extractor.extractData(loc)
		self.assertRaises(customExceptions.KeyNotFound,parseutil.parseLine_Sep,data.splitlines()[0],"testKey2")
		self.assertRaises(customExceptions.KeyNotFound,parseutil.parseLine_Sep,data.splitlines()[0],"testKey12")

		loc = self.testdir + "testCpuInfo.txt"
		data = extractor.extractData(loc)
		self.assertRaises(customExceptions.KeyNotFound,parseutil.parseLine_Sep,data.splitlines()[0],"numprocessors")

	def test_parseLine_Sep_valueDoesNotExist(self):
		"Tests parseLine_Sep with nonexistent value"
		print "ParseUtilTestCase:test_parseLine_Sep_valueDoesNotExist - begin"

		loc = self.testdir + "testParseUtil.txt"
		data = extractor.extractData(loc)
		self.assertEqual(parseutil.parseLine_Sep(data.splitlines()[2], "testKey3"), "NO_VALUE", "Value obtained from file "+ loc +" is incorrect.")
		self.assertEqual(parseutil.parseLine_Sep(data.splitlines()[5], "testKey5", ":"), "NO_VALUE", "Value obtained from file "+ loc +" is incorrect.")

		loc = self.testdir + "testCpuInfo.txt"
		data = extractor.extractData(loc)
		self.assertEqual(parseutil.parseLine_Sep(data.splitlines()[24], "power management", ":"), "NO_VALUE", "Value obtained from file "+ loc +" is incorrect.")

	def test_parseLine_Sep_sepDoesNotExist(self):
		"Tests parseLine_Sep when separator cannot be found"
		print "ParseUtilTestCase:test_parseLine_Sep_sepDoesNotExist - begin"

		loc = self.testdir + "testCpuInfo.txt"
		data = extractor.extractData(loc)
		self.assertEqual(parseutil.parseData_Sep(data.splitlines()[5],"stepping",","),"NO_VALUE", "Value obtained from file "+ loc +" is incorrect.")

		loc = self.testdir + "testParseUtil.txt"
		data = extractor.extractData(loc)
		self.assertEqual(parseutil.parseData_Sep(data.splitlines()[0],"testKey", ":"), "NO_VALUE", "Value obtained from file "+ loc +" is incorrect.")


	# -- parseData_Sep tests
	def test_parseData_Sep(self):
		"Tests parseData_Sep normal function"
		print "ParseUtilTestCase:test_parseData_Sep - begin"
		loc = self.testdir + "testParseUtil.txt"
		data = extractor.extractData(loc)
		self.assertEqual(parseutil.parseData_Sep(data, "testKey4", ":"), "testValue4", "Value obtained from file "+ loc +" is incorrect.")
		self.assertEqual(parseutil.parseData_Sep(data, "testKey2"), "testValue2 testValue2.1 testValue2.2", "Value obtained from file "+ loc +" is incorrect.")

		loc = self.testdir + "testCpuInfo.txt"
		data = extractor.extractData(loc)
		self.assertEqual(parseutil.parseData_Sep(data, "cpu cores", ":"), "4", "Value obtained from file "+ loc +" is incorrect.")

	def test_parseData_Sep_keyNotFound(self):
		"Tests parseData_Sep with inexistent key"
		print "ParseUtilTestCase:test_parseData_Sep_keyNotFound - begin"
		loc = self.testdir + "testParseUtil.txt"
		data = extractor.extractData(loc)
		self.assertRaises(customExceptions.KeyNotFound,parseutil.parseData_Sep, data,"testKeyNotExists")

		loc = self.testdir + "testCpuInfo.txt"
		data = extractor.extractData(loc)
		self.assertRaises(customExceptions.KeyNotFound,parseutil.parseData_Sep, data, "testKeyNotExists")

	def test_parseData_Sep_valueDoesNotExist(self):
		"Tests parseData_Sep to obtain value that does not exist"
		print "ParseUtilTestCase:test_parseData_Sep_valueDoesNotExist - begin"
		loc = self.testdir + "testCpuInfo.txt"
		data = extractor.extractData(loc)
		self.assertEqual(parseutil.parseData_Sep(data,"power management",":"),"NO_VALUE", "Value obtained from file "+ loc +" is incorrect.")

	def test_parseData_Sep_sepDoesNotExist(self):
		"Tests parseData_Sep when separator cannot be found"
		print "ParseUtilTestCase:test_parseData_Sep_sepDoesNotExist - begin"
		loc = self.testdir + "testCpuInfo.txt"
		data = extractor.extractData(loc)
		self.assertEqual(parseutil.parseData_Sep(data,"stepping",","),"NO_VALUE", "Value obtained from file "+ loc +" is incorrect.")

		loc = self.testdir + "testParseUtil.txt"
		data = extractor.extractData(loc)
		self.assertEqual(parseutil.parseData_Sep(data,"testKey", ":"), "NO_VALUE", "Value obtained from file "+ loc +" is incorrect.")

	# -- findLines tests
		"Tests findLines function"
		print "ParseUtilTestCase:test_findLines - begin"
		loc = self.testdir + "testParseUtil.txt"
		data = extractor.extractData(loc)
		self.assertEqual(parseutil.findLines(data, "testValue4")[0], "testKey4 : testValue4", "findLine function not working")

	# -- count tests
	def test_count(self):
		"Tests count with normal function"
		print "ParseUtilTestCase:test_count - begin"
		loc = self.testdir + "testParseUtil.txt"
		data = extractor.extractData(loc)
		self.assertEqual(parseutil.count(data,"testCount"), 6, "Value obtained from file "+ loc +" is incorrect.")
		self.assertEqual(parseutil.count(data,"testCount3"), 2, "Value obtained from file "+ loc +" is incorrect.")

	def test_count_keyNotFound(self):
		"Tests count with nonexistent key"
		print "ParseUtilTestCase:test_count_keyNotFound - begin"
		loc = self.testdir + "testParseUtil.txt"
		data = extractor.extractData(loc)
		self.assertEqual(parseutil.count(data,"testCount4"), 0, "Value obtained from file "+ loc +" is incorrect.")

	# -- PciIdsParser tests
	def test_PciIdsParser(self):
		"Tests the PciIdsParser class"
		print "ParseUtilTestCase:test_PciIdsParser - begin"
		pciIdsLoc = testpaths.PATH_TEST_PARSEUTIL + "testpciids"
		pciIdsLocMultiple = testpaths.PATH_TEST_PARSEUTIL + "testpciids_multiple"
		pciIdsLocInit = testpaths.PATH_TEST_PARSEUTIL + "testpciids_init"
		parser = parseutil.PciIdsParser(pciIdsLoc)

		#isValidVendorCode function
		self.assertEqual(parser.isValidVendorCode("0000"), True, "isValidVendorCode function not working")
		self.assertEqual(parser.isValidVendorCode("a0102"), False, "isValidVendorCodefunction not working")
		self.assertEqual(parser.isValidVendorCode("#"), False, "isValidVendorCode function not working")

		#isValidDeviceCode function
		self.assertEqual(parser.isValidVendorCode("0000"), True, "isValidDeviceCode function not working")
		self.assertEqual(parser.isValidVendorCode("12"), False, "isValidDeviceCodefunction not working")
		self.assertEqual(parser.isValidVendorCode("#"), False, "isValidDeviceCode function not working")

		#isValidClassCode function
		self.assertEqual(parser.isValidClassCode("02"), True, "isValidClassCode function not working")
		self.assertEqual(parser.isValidClassCode("0301"), False, "isValidClassCodefunction not working")
		self.assertEqual(parser.isValidClassCode("#"), False, "isValidClassCode function not working")

		#isValidSubclassCode function
		self.assertEqual(parser.isValidSubclassCode("01"), True, "isValidSubclassCode function not working")
		self.assertEqual(parser.isValidSubclassCode("a12"), False, "isValidSubclassCodefunction not working")
		self.assertEqual(parser.isValidSubclassCode("#"), False, "isValidSubclassCode function not working")

		#isVendor function
		self.assertEqual(parser.isVendor("0a12  Vendor1"), True, "isVendor function not working")
		self.assertEqual(parser.isVendor("0a12  Vendor1, Inc."), True, "isVendor function not working")
		self.assertEqual(parser.isVendor("	0a12  Vendor2"), False, "isVendor function not working")

		#isDevice function
		self.assertEqual(parser.isDevice("	0101  Device1"), True, "isDevice function not working")
		self.assertEqual(parser.isDevice("      0203  Device1_spacenottab"), False, "isDevice function not working")
		self.assertEqual(parser.isDevice("		0232  Device1"), False, "isDevice function not working")

		#isClass function
		self.assertEqual(parser.isClass("C 01  Class1"), True, "isClass function not working")
		self.assertEqual(parser.isClass("0a12 Vendor1"), False, "isClass function not working")

		#isSubclass function
		self.assertEqual(parser.isSubclass("	02  Subclass1"), True, "isSubclass function not working")
		self.assertEqual(parser.isSubclass("		02  Subsubclass"), False, "isSubclass function not working")

		#init function
		parser_init = parseutil.PciIdsParser(pciIdsLocInit)
		self.assertEqual(len(parser_init.vendorData), 6, "PciIdsParser not initialised properly")
		self.assertEqual(len(parser_init.deviceData), 3, "PciIdsParser not initialised properly")
		self.assertEqual(len(parser_init.classData), 10, "PciIdsParser not initialised properly")

		self.assertRaises(customExceptions.PciIdsMultipleEntries, parseutil.PciIdsParser, pciIdsLocMultiple)

		#getVendorName function
		self.assertEqual(parser.getVendorName("0x0e11"), "Compaq Computer Corporation", "getVendorName function not working")
		self.assertRaises(customExceptions.PciIdsFailedSearch, parser.getVendorName, "0x0400")

		#getDeviceName function
		self.assertEqual(parser.getDeviceName("0x0675", "0x1700"), "IS64PH ISDN Adapter", "getDeviceName function not working")
		self.assertEqual(parser.getDeviceName("0x0675", "0x1704"), "ISDN Adapter (PCI Bus, D, C)", "getDeviceName function not working")
		self.assertEqual(parser.getDeviceName("0x8086", "0x0108"), "Xeon E3-1200 Processor Family DRAM Controller", "getDeviceName function not working")
		self.assertRaises(customExceptions.PciIdsFailedSearch, parser.getDeviceName, "0x0675", "0x2000")

		#getClassName function
		self.assertEqual(parser.getClassName("0x0604"), "PCI bridge", "getClassName function not working")
		self.assertEqual(parser.getClassName("0x0c06"), "InfiniBand", "getClassName function not working")
		self.assertEqual(parser.getClassName("0x0608"), "RACEway bridge", "getClassName function not working")
		self.assertEqual(parser.getClassName("0x0600"), "Host bridge", "getClassName function not working")
		self.assertRaises(customExceptions.PciIdsSubclassNotFound, parser.getClassName, "0x0685")
		self.assertRaises(customExceptions.PciIdsFailedSearch, parser.getClassName, "0x1400")

# == Runs the Unit Test ==
if __name__ == "__main__":
	unittest.main()
