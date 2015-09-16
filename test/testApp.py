#   Copyright (C) 2015 Chen Chin Jieh <cchen@hsr.ch>
#
#   This file is part of mugenplcfg.
#
#   mugenplcfg is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   mugenplcfg is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with mugenplcfg.  If not, see <http://www.gnu.org/licenses/>.


# Module that runs test cases with PyUnit
import sys
sys.dont_write_bytecode = True
import unittest
import os
# Add parent directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import testpaths
import paths
import mock
import shutil
import subprocess
from src import customExceptions
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

    # -- extractData testcases
    def test_extractData(self):
        "Tests the extractData function"
        print "ExtractorTestCase:test_extractData - begin"

        loc = self.testdir + "testExtractData.txt"
        self.assertEqual(extractor.extractData(loc), "test",
                         "Extracted Data from file " + loc + " does not match.")
        self.assertNotEqual(extractor.extractData(loc), "test2",
                            "Extracted Data from file " + loc + " matches incorrectly.")
        self.assertNotEqual(extractor.extractData(loc), "",
                            "Extracted Data from file " + loc + " matches incorrectly.")

    def test_extractData_blank(self):
        "Tests the extractData function with blank file"
        print "ExtractorTestCase:test_extractData_blank - begin"

        loc = self.testdir + "testExtractData_blank.txt"
        self.assertEqual(extractor.extractData(loc), "",
                         "Extracted Data from file " + loc + " does not match.")

    def test_extractData_doesNotExist(self):
        "Tests the extractData function with file that does not exist"
        print "ExtractorTestCase:test_extractData_doesNotExist - begin"

        loc = self.testdir + "testExtractData_shouldnotexist.txt"
        self.assertRaises(IOError, extractor.extractData, loc)

    # -- extractBinaryData testcases
    def test_extractBinaryData(self):
        "Tests the extractBinaryData function"
        print "ExtractorTestCase:test_extractBinaryData - begin"
        loc = testpaths.PATH_TEST_GEN + "testExtractBinaryData"
        with open(loc, "wb") as f:
            f.write(b"\x01\x02\x03\x04")
        self.assertEqual(extractor.extractBinaryData(loc, 0, 4),
                         "0x04030201", "extractBinaryData function not working")
        self.assertEqual(extractor.extractBinaryData(loc, 0, 4, chunks=True), [
                         "0x04", "0x03", "0x02", "0x01"], "extractBinaryData function not working")
        self.assertEqual(extractor.extractBinaryData(loc, 2, 2, chunks=True), [
                         "0x04", "0x03"], "extractBinaryData function not working")
        self.assertEqual(extractor.extractBinaryData(loc, 0, 2, "LITTLE_ENDIAN", chunks=True), [
                         "0x01", "0x02"], "extractBinaryData function not working")
        self.assertRaises(
            customExceptions.NoAccessToFile, extractor.extractBinaryData, loc, 3, 2)
        self.assertRaises(
            ValueError, extractor.extractBinaryData, loc, 0, 4, "MIDDLE_ENDIAN", chunks=True)

# == creator.py tests ==
import src.creator as creator

class CreatorTestCase(unittest.TestCase):
    
    "Tests the creator.py module"
    
    def setUp(self):
        print "<> CreatorTestCase:setUp - begin"
        self.testdir = testpaths.PATH_TEST_CREATOR

    def tearDown(self):
        print "<> CreatorTestCase:tearDown - begin"
        
    def test_genDmesg(self):
        print "CreatorTestCase:test_genDmesg - begin"
        gen = testpaths.PATH_TEST_GEN
        creator.genDmesg(gen, "test_genDmesg")
        self.assertTrue(os.path.isfile(os.path.join(gen,"test_genDmesg")))
    
class ProcessorCreatorTestCase(unittest.TestCase):

    "Tests the ProcessorCreator class"

    def setUp(self):
        print "<> ProcessorCreatorTestCase:setUp - begin"
        self.testdir = os.path.join(
            testpaths.PATH_TEST_CREATOR, "processorcreator")
        self.procreator = creator.ProcessorCreator()

    def tearDown(self):
        print "<> ProcessorCreatorTestCase:tearDown - begin"

    def test_createElem(self):
        print "ProcessorCreatorTestCase:test_createElem - begin"
        cpuinfo = os.path.join(self.testdir, "cpuinfo")
        msr = os.path.join(testpaths.PATH_TEST_GEN, "msr")
        dmesg = os.path.join(self.testdir, "dmesg")

        processor = Element("processor", "processorType")
        processor["logicalCpus", "speed", "vmxTimerRate"] = 8, 3193, 5

        VMX_OFFSET = 0x485
        VMX_BITSIZE = 5
        with open(msr, "wb") as f:
            f.seek(VMX_OFFSET)
            f.write(b"\x05\x0e")

        result = self.procreator.createElem(cpuinfo, [msr], dmesg)
        self.assertEqual(
            result.isEqual(processor), True, "createElems not working")
        processor.toXML("utf-8")

    def test_getLogicalCpus(self):
        print "ProcessorCreatorTestCase:test_getLogicalCpus - begin"
        cpuinfoloc = os.path.join(self.testdir, "cpuinfo")
        self.assertEqual(
            self.procreator.getLogicalCpus(cpuinfoloc), 8,
            "getLogicalCpus function not working")

    def test_getSpeed(self):
        print "ProcessorCreatorTestCase:test_getSpeed - begin"
        dmesgloc = os.path.join(self.testdir, "dmesg")
        dmesg_nokey = os.path.join(self.testdir, "dmesg_nokey")
        invalidloc = os.path.join(self.testdir, "invalidlocdmesg")
        KEY = "Refined TSC clocksource calibration"
        self.assertEqual(self.procreator.getSpeed(dmesgloc), 3192.746,
                         "getSpeed function not working")
        self.assertRaises(customExceptions.ForceQuit,
                          self.procreator.getSpeed,
                          invalidloc )
        self.assertRaises(customExceptions.ForceQuit,
                          self.procreator.getSpeed,
                          dmesg_nokey )
        

    def test_getVmxTimerRate(self):
        print "ProcessorCreatorTestCase:test_getVmxTimerRate - begin"
        msrpath1 = os.path.join(testpaths.PATH_TEST_GEN, "testmsr_path1")
        msrpath_invalid = "invalidpath"
        msrpathlist = [msrpath_invalid]
        OFFSET = 0
        VMX_BITSIZE = 5
        self.assertRaises(customExceptions.ForceQuit,
                          self.procreator.getVmxTimerRate,
                          msrpathlist, OFFSET, VMX_BITSIZE)

        with open(msrpath1, "wb") as f:
            f.write(b"\x01\x02\x03\x04")
        msrpathlist.append(msrpath1)

        self.assertEqual(
            self.procreator.getVmxTimerRate(msrpathlist, OFFSET, VMX_BITSIZE),
            1,
            "getVmxTimerRate function not working")

    def test_getVmxFromMSR(self):
        print "ProcessorCreatorTestCase:test_getVmxFromMSR - begin"
        msrpath = os.path.join(testpaths.PATH_TEST_GEN, "testmsr")
        with open(msrpath, "wb") as f:
            f.write(b"\x01\x02\x03\x04")
        OFFSET = 0
        VMX_BITSIZE = 5
        self.assertEqual(self.procreator.getVmxFromMSR(
            msrpath, OFFSET, VMX_BITSIZE), 1, "getVmxFromMSR function not working")
        with open(msrpath, "wb") as f:
            f.write(b"\x05\x02\x03\x04")
        self.assertEqual(self.procreator.getVmxFromMSR(
            msrpath, OFFSET, VMX_BITSIZE), 5, "getVmxFromMSR function not working")
        with open(msrpath, "wb") as f:
            f.write(b"\x11\x02\x03\x04")
        self.assertEqual(self.procreator.getVmxFromMSR(
            msrpath, OFFSET, VMX_BITSIZE), 17, "getVmxFromMSR function not working")
        msrinvalidpath = os.path.join(self.testdir, "testmsr_invalid")
        self.assertRaises(
            IOError, self.procreator.getVmxFromMSR, msrinvalidpath, OFFSET, VMX_BITSIZE)


class MemoryCreatorTestCase(unittest.TestCase):

    "Tests the MemoryCreator class"

    def setUp(self):
        print "<> MemoryCreatorTestCase:setUp - begin"
        self.testdir = os.path.join(
            testpaths.PATH_TEST_CREATOR, "memorycreator")
        self.memcreator = creator.MemoryCreator()

    def tearDown(self):
        print "<> MemoryCreatorTestCase:tearDown - begin"
        result = self.memcreator.createElem(
            os.path.join(self.testdir, "memmap"))

    def test_createElem(self):
        print "MemoryCreatorTestCase:test_createElem - begin"

    def test_memmapextraction(self):
        "Tests various functions related to memmap extraction"
        print "MemoryCreatorTestCase:test_memmapextraction - begin"

        loc = os.path.join(self.testdir, "memmap")
        invalidloc = os.path.join(self.testdir, "memmap_invalid")
        incompleteloc = os.path.join(self.testdir, "memmap_incomplete")

        # Test isAllocatable function
        memblock_1 = Element("memoryBlock", "memoryBlockType")
        memblock_1["name", "physicalAddress"] = "System RAM", "16#0010_000f#"

        memblock_2 = Element("memoryBlock", "memoryBlockType")
        memblock_2["name", "physicalAddress"] = "System RAM2", "16#0010_000f"

        memblock_3 = Element("memoryBlock", "memoryBlockType")
        memblock_3["name", "physicalAddress"] = "System RAM", "0xfffff"

        memblock_4 = Element("memoryBlock", "memoryBlockType")
        memblock_4["name", "physicalAddress"] = "System RAM2", "0x1000"
        self.assertEqual(self.memcreator.isAllocatable(
            memblock_1), True, "isAllocatable function is not working")
        self.assertEqual(self.memcreator.isAllocatable(
            memblock_2), False, "isAllocatable function is not working")
        self.assertEqual(self.memcreator.isAllocatable(
            memblock_3), False, "isAllocatable function is not working")
        self.assertEqual(self.memcreator.isAllocatable(
            memblock_4), False, "isAllocatable function is not working")

        # Test getMemoryBlocks
        memoryBlockList_invalid = self.memcreator.getMemoryBlocks(invalidloc)
        memoryBlockList_incomplete = self.memcreator.getMemoryBlocks(
            incompleteloc)
        memoryBlockList = self.memcreator.getMemoryBlocks(loc)
        memoryBlock0 = memoryBlockList[0].compileToPyxb()
        memoryBlock1 = memoryBlockList[1].compileToPyxb()
        self.assertEqual(memoryBlock0.physicalAddress,
                         "16#000a#", "getMemoryBlocks function not working")
        self.assertEqual(
            memoryBlock0.size, "16#f000#", "getMemoryBlocks function not working")
        self.assertEqual(
            memoryBlock1.name, "1_type", "getMemoryBlocks function not working")

        # Test generateMemoryBlock
        startfile = os.path.join(loc, "0/start")
        startfile_invalid = os.path.join(loc, "0/start_invalid")
        endfile = os.path.join(loc, "0/end")
        typefile = os.path.join(loc, "0/type")

        memoryBlock = self.memcreator.generateMemoryBlock(
            endfile, typefile, startfile)
        memoryBlock_pyxb = memoryBlock.compileToPyxb()
        self.assertEqual(
            memoryBlock_pyxb.name, "0_type", "generateMemoryBlock not working")
        self.assertEqual(memoryBlock_pyxb.physicalAddress,
                         "16#000a#", "generateMemoryBlock not working")
        self.assertRaises(IOError,
                          self.memcreator.generateMemoryBlock,
                          endfile, typefile, startfile_invalid)
        
        def isAllocatable_true(memBlock):
            return True
        
        @mock.patch.object(self.memcreator, "isAllocatable", isAllocatable_true)
        def mock_testAllocatable():
            return self.memcreator.generateMemoryBlock(endfile,
                                                       typefile,
                                                       startfile)
        mockmemblock = mock_testAllocatable()
        self.assertEqual(mockmemblock["allocatable"], "true", "generateMemoryBlock not working")


class DevicesCreatorTestCase(unittest.TestCase):

    "Tests the DevicesCreator class"

    def setUp(self):
        print "<> DevicesCreatorTestCase:setUp - begin"
        self.testdir = os.path.join(
            testpaths.PATH_TEST_CREATOR, "devicescreator")
        self.devcreator = creator.DevicesCreator()

    def tearDown(self):
        print "<> DevicesCreatorTestCase:tearDown - begin"
        
    def test_createElem(self):
        print "DevicesCreatorTestCase:test_createElem - begin"
        def mock_IommuDevicesCreator_createElems(arg, *args, **kwargs):
            return [Element("device", "deviceType")]
        def mock_SerialDevicesCreator_createElems(arg, *args,**kwargs):
            return [Element("device", "deviceType")]
        def mock_PciDevicesCreator_createElems(arg, *args, **kwargs):
            return [Element("device", "deviceType")]
        
        @mock.patch.object(creator.IommuDevicesCreator, "createElems",
                           mock_IommuDevicesCreator_createElems)
        @mock.patch.object(creator.SerialDevicesCreator, "createElems",
                           mock_SerialDevicesCreator_createElems)
        @mock.patch.object(creator.PciDevicesCreator, "createElems",
                           mock_PciDevicesCreator_createElems)
        def mock_createElem():
            iomem = os.path.join(self.testdir, "test_iomem")
            return self.devcreator.createElem()
            
        mockelem = mock_createElem()
        self.assertEqual(len(mockelem.childElements), 3, "createElem not working")   

    def test_getPciConfigAddress(self):
        print "DevicesCreatorTestCase:test_getPciConfigAddress - begin"
        testiomem = os.path.join(self.testdir, "test_iomem")
        testinvalidloc = os.path.join(
            self.testdir, "testgetpciconfig_invalidloc")
        testnokey = os.path.join(self.testdir, "test_iomem_nopciconfig")
        self.assertEqual(self.devcreator.getPciConfigAddress(
            testiomem), "e0000000", "getPciConfigAddress function not working")
        self.devcreator.getPciConfigAddress(testinvalidloc)
        self.devcreator.getPciConfigAddress(testnokey)


class PciDevicesCreatorTestCase(unittest.TestCase):

    "Tests the PciDevicesCreator class"

    def setUp(self):
        print "<> PciDevicesCreatorTestCase:setUp - begin"
        self.testdir = os.path.join(
            testpaths.PATH_TEST_CREATOR, "devicescreator")
        self.devloc = os.path.join(self.testdir, "devices")
        self.devtree = os.path.join(self.testdir, "devices_test")
        self.devicesdir = testpaths.PATH_DEVICELINKS
        self.pcicreator = creator.PciDevicesCreator()

    def tearDown(self):
        print "<> PciDevicesCreatorTestCase:tearDown - begin"

    def test_createElems(self):
        print "PciDevicesCreatorTestCase:test_createElems - begin"
        devicesdir = os.path.join(self.testdir, "devices_test_links")
        self.assertEqual(len(self.pcicreator.createElems(devicesdir)),
                         12,
                         "createElems function not working")

    def test_init_DevicecapManager(self):
        print "PciDevicesCreatorTestCase:test_init_DevicecapManager - begin"
        testloc = self.devtree
        devices = os.listdir(testloc)
        devicepaths = []
        for devicename in devices:
            devicepaths.append(os.path.join(testloc, devicename))

        self.pcicreator.init_DevicecapManager(devicepaths)
        devicecapmgr_invalid = self.pcicreator.init_DevicecapManager(
            "invaliddevicepaths")
        self.assertEqual(
            len(devicecapmgr_invalid.getCapabilities()), 0, "init_DevicecapManager not working")

    def test_filterDevicePaths(self):
        print "PciDevicesCreatorTestCase:test_filterDevicePaths - begin"
        testloc = self.devtree
        devices = os.listdir(testloc)
        devicepaths = []
        for devicename in devices:
            devicepaths.append(os.path.join(testloc, devicename))
        """
		devicepaths.append(os.path.join(testloc,"0000:00:01.0/0000:01:00.0"))
		devicepaths.append(os.path.join(testloc,"0000:00:01.0/0000:01:00.1"))
		devicepaths.append(os.path.join(testloc,"0000:00:1c.4/0000:03:00.0"))
		"""

        devicecapmgr = devicecap.DevicecapManager()
        devicecapmgr.extractCapabilities(devicepaths)

        self.assertEqual(
            len(self.pcicreator.filterDevicePaths(
                devicepaths, devicecapmgr)),
            12,
            "filterDevicePaths not working")

    def test_isDeviceName(self):
        print "PciDevicesCreatorTestCase:test_isDeviceName - begin"
        self.assertEqual(self.pcicreator.isDeviceName(
            "0000:01:00.0"), True, "isDeviceName function not working")
        self.assertEqual(self.pcicreator.isDeviceName(
            "0000:00:01.2"), True, "isDeviceName function not working")
        self.assertEqual(self.pcicreator.isDeviceName(
            "0001:17:02.5"), True, "isDeviceName function not working")
        self.assertEqual(self.pcicreator.isDeviceName(
            "010:10:01.2"), False, "isDeviceName function not working")
        self.assertEqual(self.pcicreator.isDeviceName(
            "0000:10:01"), False, "isDeviceName function not working")
        self.assertEqual(self.pcicreator.isDeviceName(
            "000:10:01.1"), False, "isDeviceName function not working")
        self.assertEqual(self.pcicreator.isDeviceName(
            "000:10:010.1"), False, "isDeviceName function not working")
        self.assertEqual(self.pcicreator.isDeviceName(
            "000:10:01.11"), False, "isDeviceName function not working")
        self.assertEqual(self.pcicreator.isDeviceName(
            "000:10:01:00.1"), False, "isDeviceName function not working")
        self.assertEqual(self.pcicreator.isDeviceName(
            "0003:0E0F:0003.0001"), False, "isDeviceName function not working")

    def test_isBridge(self):
        print "PciDevicesCreatorTestCase:test_isBridge - begin"
        self.assertEqual(self.pcicreator.isBridge(
            os.path.join(self.devloc, "pcibridge0")), True, "isBridge function not working")
        self.assertEqual(self.pcicreator.isBridge(
            os.path.join(self.devloc, "dev0")), False, "isBridge function not working")

    def test_isPciExpress(self):
        print "PciDevicesCreatorTestCase:test_isPciExpress - begin"
        dev0 = os.path.join(self.testdir, "devices_testcap/dev0")
        dev1 = os.path.join(self.testdir, "devices_testcap/dev1")
        devicecapmgr = devicecap.DevicecapManager()
        devicecapmgr.extractCapabilities([dev0, dev1])
        self.assertEqual(self.pcicreator.isPciExpress(dev0, devicecapmgr),
                         True,
                         "isPciExpress function not working")
        self.assertEqual(self.pcicreator.isPciExpress(dev1, devicecapmgr),
                         False,
                         "isPciExpress function not working")

    def test_getDeviceBus(self):
        print "PciDevicesCreatorTestCase:test_getDeviceBus - begin"
        self.assertEqual(self.pcicreator.getDeviceBus(
            "0011:01:02.3"), "01", "getDeviceBus function not working")

    def test_getDeviceNo(self):
        print "PciDevicesCreatorTestCase:test_getDeviceNo - begin"
        self.assertEqual(self.pcicreator.getDeviceNo(
            "0000:01:02.3"), "02", "getDeviceNo function not working")

    def test_getDeviceFunction(self):
        print "PciDevicesCreatorTestCase:test_getDeviceFunction - begin"
        self.assertEqual(self.pcicreator.getDeviceFunction(
            "0000:01:02.3"), "3", "getDeviceFunction function not working")

    def test_getDeviceShortNames(self):
        print "PciDevicesCreatorTestCase:test_getDeviceShortNames - begin"
        testpciids = testpaths.PATH_PCIIDS
        devdir = os.path.join(self.testdir, "devices_testshortnames")
        devpaths = []
        for dir in sorted(os.listdir(devdir)):
            devpaths.append(os.path.join(devdir, dir))
        testresult = {
            os.path.join(devdir, "dev0"): "host_bridge",
            os.path.join(devdir, "dev1"): "0x06ff00",
            os.path.join(devdir, "dev2"): "pci_bridge"
        }

        result = self.pcicreator.getDeviceShortNames(devpaths, testpciids)
        self.assertEqual(result, testresult, "getDeviceShortNames not working")
        self.assertEqual(
            len(self.pcicreator.getDeviceShortNames(
                devpaths, "invalidpciidsloc")),
            0,
            "getDeviceShortNames not working")

    def test_getClassName(self):
        print "PciDevicesCreatorTestCase:test_getClassName - begin"
        testpciids = testpaths.PATH_PCIIDS
        pciidsparser = parseutil.PciIdsParser(testpciids)
        devpath = os.path.join(self.testdir, "devices/dev0")
        devpath_invalidclass = os.path.join(
            self.testdir, "devices/dev_invalidclass")
        self.assertEqual(self.pcicreator.getClassName(devpath, pciidsparser),
                         "host_bridge",
                         "getClassName function not working")
        self.assertEqual(
            self.pcicreator.getClassName(devpath_invalidclass, pciidsparser),
            "0x06ff00",
            "getClassName function not working")

    def test_getPci(self):
        print "PciDevicesCreatorTestCase:test_getPci - begin"
        testloc = os.path.join(self.testdir, "devices_testcap")
        devicecapmgr = devicecap.DevicecapManager()
        dev = os.path.join(testloc, "0000:01:02.3")
        devicecapmgr.extractCapabilities([dev])

        dev_pci = self.pcicreator.getPci(dev, devicecapmgr)
        self.assertEqual(
            dev_pci["bus"], "16#01#", "getPci function not working")
        self.assertEqual(
            dev_pci["function"], "3", "getPci function not working")
        self.assertEqual(
            dev_pci["device"], "16#02#", "getPci function not working")

    def test_getPci_MSI(self):
        print "PciDevicesCreatorTestCase:test_getPci_MSI - begin"
        testloc = os.path.join(self.testdir, "devices_testcap")
        devicecapmgr = devicecap.DevicecapManager()
        dev0 = os.path.join(testloc, "dev0")
        dev1 = os.path.join(testloc, "dev1")
        dev2 = os.path.join(testloc, "dev2")
        devicelist = [dev0, dev1, dev2	]
        devicecapmgr.extractCapabilities(devicelist)

        self.assertEqual(self.pcicreator.getPci_MSI(dev0, devicecapmgr),
                         "true",
                         "_getPci_MSI function not working")
        self.assertEqual(self.pcicreator.getPci_MSI(dev1, devicecapmgr),
                         "true",
                         "_getPci_MSI function not working")
        self.assertEqual(self.pcicreator.getPci_MSI(dev2, devicecapmgr),
                         "false",
                         "_getPci_MSI function not working")

    def test_getIrq(self):
        print "PciDevicesCreatorTestCase:test_getIrq - begin"
        testloc = os.path.join(self.testdir, "devices_testirq")
        dev0 = os.path.join(testloc, "dev0")
        dev1 = os.path.join(testloc, "dev1")
        dev_invalid = "test_getirq_invalid"

        dev0_irq = self.pcicreator.getIrq(dev0)
        dev1_irq = self.pcicreator.getIrq(dev1)
        dev_invalid_irq = self.pcicreator.getIrq(dev_invalid)

        self.assertEqual(
            dev1_irq["number"], "15", "getIrq function not working")
        self.assertEqual(dev0_irq, None, "getIrqfunction not working")
        self.assertEqual(dev_invalid_irq, None, "getIrqfunction not working")

    def test_getDeviceMemoryBlocks(self):
        print "PciDevicesCreatorTestCase:test_getDeviceMemoryBlocks - begin"
        testloc = os.path.join(self.testdir, "devices_testresource")

        Memblock = namedtuple("Memblock", ["name", "start", "size"])

        # No filter: actual data
        dev0_loc = os.path.join(testloc, "dev0")
        dev2_loc = os.path.join(testloc, "dev2")
        dev_emptyresource = os.path.join(testloc, "dev_emptyresource")
        dev_invalidresource = os.path.join(testloc, "dev_invalidresource")

        dev0_testmemblock_nofilter = [
            Memblock(name="mem0", start="16#fb22_5000#", size="16#0800#")]
        dev2_testmemblock_nofilter = [
            Memblock(
                name="mem0", start="16#fb20_0000#", size="16#0002_0000#"),
            Memblock(name="mem1", start="16#fb22_8000#", size="16#1000#")
        ]

        NOFILTERSIZE = "0x0"
        dev0_memblocks_nofilter = self.pcicreator.getDeviceMemoryBlocks(
            dev0_loc, NOFILTERSIZE)
        dev2_memblocks_nofilter = self.pcicreator.getDeviceMemoryBlocks(
            dev2_loc, NOFILTERSIZE)

        dev0_memblocktuplelist_nofilter = []
        for memblock in dev0_memblocks_nofilter:
            dev0_memblocktuplelist_nofilter.append(
                Memblock(name=memblock["name"],
                         start=memblock["physicalAddress"],
                         size=memblock["size"])
            )
        dev2_memblocktuplelist_nofilter = []
        for memblock in dev2_memblocks_nofilter:
            dev2_memblocktuplelist_nofilter.append(
                Memblock(name=memblock["name"],
                         start=memblock["physicalAddress"],
                         size=memblock["size"])
            )

        self.assertEqual(dev0_memblocktuplelist_nofilter,
                         dev0_testmemblock_nofilter, "getDeviceMemoryBlocks not working")
        self.assertEqual(dev2_memblocktuplelist_nofilter,
                         dev2_testmemblock_nofilter, "getDeviceMemoryBlocks not working")

        # Filter on
        dev0_testmemblock_filter = [
            Memblock(name="mem0", start="16#fb22_5000#", size="16#1000#")]
        dev0_memblocks_filter = self.pcicreator.getDeviceMemoryBlocks(dev0_loc)
        dev0_memblocktuplelist_filter = []
        for memblock in dev0_memblocks_filter:
            dev0_memblocktuplelist_filter.append(
                Memblock(name=memblock["name"],
                         start=memblock["physicalAddress"],
                         size=memblock["size"])
            )

        self.assertEqual(dev0_memblocktuplelist_filter,
                         dev0_testmemblock_filter, "getDeviceMemoryBlocks not working")

        # Test empty resource
        dev_emptyresource_list = self.pcicreator.getDeviceMemoryBlocks(
            dev_emptyresource)
        self.assertEqual(
            dev_emptyresource_list, [], "getDeviceMemoryBlocks not working")

        # Test invalid resource
        dev_invalidresourcelist = self.pcicreator.getDeviceMemoryBlocks(
            dev_invalidresource)
        self.assertEqual(
            dev_invalidresourcelist, [], "getDeviceMemoryBlocks not working")

    def test_getIoports(self):
        print "PciDevicesCreatorTestCase:test_getIoports - begin"
        testloc = os.path.join(self.testdir, "devices_testresource")
        dev0_loc = os.path.join(testloc, "dev0")
        dev1_loc = os.path.join(testloc, "dev1")
        dev_noresource = os.path.join(testloc, "dev_noresource")
        dev_emptyresource = os.path.join(testloc, "dev_emptyresource")
        Ioport = namedtuple("Ioport", ["name", "start", "end"])
        dev0_testioports = [
            Ioport("ioport0", "16#f090#", "16#f097#"),
            Ioport("ioport1", "16#f080#", "16#f083#"),
            Ioport("ioport2", "16#f070#", "16#f077#"),
            Ioport("ioport3", "16#f060#", "16#f063#"),
            Ioport("ioport4", "16#f020#", "16#f03f#")
        ]
        dev1_testioports = []
        dev_emptyresource_testioports = []

        dev0_ioports = self.pcicreator.getIoports(dev0_loc)
        dev1_ioports = self.pcicreator.getIoports(dev1_loc)
        dev_emptyresource_ioports = self.pcicreator.getIoports(
            dev_emptyresource)

        dev0_ioport_tuplelist = []
        for ioport in dev0_ioports:
            iotuple = Ioport(name=ioport["name"],
                             start=ioport["start"],
                             end=ioport["end"])
            dev0_ioport_tuplelist.append(iotuple)

        self.assertEqual(
            dev0_ioport_tuplelist, dev0_testioports, "getIoports function not working")
        self.assertEqual(
            dev1_ioports, dev1_testioports, "getIoports function not working")
        self.assertEqual(dev_emptyresource_ioports,
                         dev_emptyresource_testioports, "getIoports function not working")
        self.assertEqual(self.pcicreator.getIoports(
            dev_noresource), [], "getIoports function not working")

    def test_createDeviceFromPath(self):
        print "PciDevicesCreator:test_createDeviceFromPath - begin"
        testloc = os.path.join(self.testdir, "devices_test")
        devpath = os.path.join(testloc, "0000:00:1f.3")

        devcapmgr = devicecap.DevicecapManager()
        devcapmgr.extractCapabilities([devpath])
        devshortnames = self.pcicreator.getDeviceShortNames(
            [devpath], testpaths.PATH_PCIIDS)
        resultdev = self.pcicreator.createDeviceFromPath(
            devpath, devcapmgr, devshortnames)

        device = Element("device", "deviceType")
        device["name"] = "smbus"
        # pci
        pci = Element("pci", "pciType")
        pci["bus", "device", "function", "msi"] = ("16#00#",
                                                   "16#1f#",
                                                   "3",
                                                   "false")
        irq = Element("irq", "irqType")
        irq["name", "number"] = "irq", "3"

        memory = Element("memory", "deviceMemoryType")
        memory["caching", "name", "physicalAddress", "size"] = ("UC",
                                                                "mem0",
                                                                "16#fb22_4000#",
                                                                "16#1000#")
        ioport = Element("ioPort", "ioPortType")
        ioport["end", "name", "start"] = "16#f01f#", "ioport0", "16#f000#"

        device.appendChild(pci, irq, memory, ioport)

        self.assertEqual(
            resultdev.isEqual(device), True, "createDeviceFromPath not working")


class SerialDevicesCreatorTestCase(unittest.TestCase):

    "Tests the SerialDevicesCreator class"

    def setUp(self):
        print "<> SerialDevicesCreatorTestCase:setUp - begin"
        self.testdir = os.path.join(
            testpaths.PATH_TEST_CREATOR, "devicescreator")
        self.serialcreator = creator.SerialDevicesCreator()

    def tearDown(self):
        print "<> SerialDevicesCreatorTestCase:tearDown - begin"

    def test_createElems(self):
        print "SerialDevicesCreator:test_createElems - begin"
        ioportloc = testpaths.PATH_IOPORTS
        result = self.serialcreator.createElems(ioportloc)

        device = Element("device", "deviceType")
        device["name"] = "com_1"

        ioport = Element("ioPort", "ioPortType")
        ioport["end", "name", "start"] = "16#03ff#", "ioport", "16#03f8#"
        device.appendChild(ioport)

        self.assertEqual(
            result[0].isEqual(device), True, "createElems not working")

    # -- SerialDevicesCreator testcases
    def test_getSerialAddresses(self):
        print "SerialDevicesCreator:test_getSerialAddresses - begin"
        ioportloc = os.path.join(self.testdir, "test_ioports")
        ioportloc_nokey = os.path.join(self.testdir, "test_ioports_nokey")
        self.assertEqual(self.serialcreator.getSerialAddresses(ioportloc),
                         [("03f8", "03ff"), (
                          "0ff0", "0ff8"), ("0ff9", "0fff")],
                         "getSerialAddresses function not working")
        self.assertEqual(
            self.serialcreator.getSerialAddresses(
                "test_ioport_invalid_location"),
            [],
            "getSerialAddresses function not working")
        self.assertEqual(
            self.serialcreator.getSerialAddresses(ioportloc_nokey),
            [],
            "getSerialAddresses function not working")

    def test_createComDevices(self):
        print "SerialDevicesCreator:test_createComDevices - begin"
        Address = namedtuple("Address", ["start", "end"])
        comAddresses = {
            Address("03f8", "03ff"): "com_1",
            Address("02f8", "02ff"): "com_2",
            Address("03e8", "03ef"): "com_3",
            Address("02e8", "02ef"): "com_4"
        }
        serialAddresses = [
            Address("03e8", "03ef"),
            Address("0ff0", "0fff"),
            Address("02f8", "02ff"),
            Address("03f8", "03ff"),
            Address("02e8", "02ef")
        ]

        testresult = ["com_1", "com_2", "com_3", "com_4"]
        comdev = self.serialcreator.createComDevices(
            serialAddresses, comAddresses)
        names = []
        for dev in comdev:
            names.append(dev["name"])

        self.assertEqual(
            set(names), set(testresult), "createComDevices not working")

    def test_createSerialDevices(self):
        print "SerialDevicesCreator:test_createSerialDevices - begin"
        Address = namedtuple("Address", ["start", "end"])
        serialAddresses = [
            Address("03e8", "03ef"),
            Address("0ff0", "0fff"),
            Address("02f8", "02ff"),
        ]
        testresult = ["serial_0", "serial_1", "serial_2"]
        serialdev = self.serialcreator.createSerialDevices(serialAddresses)
        names = []
        for dev in serialdev:
            names.append(dev["name"])
        self.assertEqual(
            set(names), set(testresult), "createSerialDevices not working")

    def test_getAddressFromLine(self):
        print "SerialDevicesCreator:test_getAddressFromLine - begin"
        self.assertEqual(self.serialcreator.getAddressFromLine("  3e0f-3e50 : serial"), (
            "3e0f", "3e50"), "getAddressFromLine function not working")
        self.assertEqual(self.serialcreator.getAddressFromLine("    3e05-3e10 : serial"), (
            "3e05", "3e10"), "getAddressFromLine function not working")


class IommuDevicesCreatorTestCase(unittest.TestCase):

    "Tests the IommuDevicesCreator class"

    def setUp(self):
        print "<> IommuDevicesCreatorTestCase:setUp - begin"
        self.testdir = os.path.join(
            testpaths.PATH_TEST_CREATOR, "devicescreator")
        self.iommucreator = creator.IommuDevicesCreator()

    def tearDown(self):
        print "<> IommuDevicesCreatorTestCase:tearDown - begin"

    def test_createElems(self):
        print "IommuDevicesCreatorTestCase:createElems - begin"
        def mock_dmarparser_genDMAR(arg, *args, **kwargs):
            return True
        def mock_dmarparser_parseDMAR(arg, *args, **kwargs):
            return True
        def mock_dmarparser_getIommuAddrs(arg, *args, **kwargs):
            return ["e00000"]
        def mock_createDeviceFromAddr(arg, *args, **kwargs):
            return Element("device", "deviceType")
        
        @mock.patch.object(parseutil.DMARParser, "genDMAR",
                           mock_dmarparser_genDMAR)
        @mock.patch.object(parseutil.DMARParser, "parseDMAR",
                           mock_dmarparser_parseDMAR)
        @mock.patch.object(parseutil.DMARParser, "getIommuAddrs",
                           mock_dmarparser_getIommuAddrs)
        @mock.patch.object(creator.IommuDevicesCreator, "createDeviceFromAddr",
                           mock_createDeviceFromAddr)
        def mock_createElems():
            return self.iommucreator.createElems("dmarpath","temppath","devmem")
        
        mock_createElems()

    def test_getIommuAGAW(self):
        print "IommuDevicesCreatorTestCase:test_getIommuAGAW - begin"
        testdevmem = os.path.join(testpaths.PATH_TEST_GEN, "testdevmem")
        testdevmem_invalid = "test_devmem_invalid"
        IOMMUADDR = "0x0"
        CAP_OFFSET = "0x0"
        CAP_REG_BYTE_SIZE = 3
        AGAW_BIT_START = 0

        with open(testdevmem, "wb") as f:
            f.write(b"\x02\x02\x03\x04")
        self.assertEqual(self.iommucreator.getIommuAGAW(IOMMUADDR,
                                                        testdevmem,
                                                        CAP_OFFSET,
                                                        CAP_REG_BYTE_SIZE,
                                                        AGAW_BIT_START),
                         "39",
                         "getIommuAGAW function not working")

        with open(testdevmem, "wb") as f:
            f.write(b"\x04\x02\x03\x04")
        self.assertEqual(self.iommucreator.getIommuAGAW(IOMMUADDR,
                                                        testdevmem,
                                                        CAP_OFFSET,
                                                        CAP_REG_BYTE_SIZE,
                                                        AGAW_BIT_START),
                         "48",
                         "getIommuAGAW function not working")
        with open(testdevmem, "wb") as f:
            f.write(b"\x01\x02\x03\x04")
        self.assertEqual(self.iommucreator.getIommuAGAW(IOMMUADDR,
                                                        testdevmem,
                                                        CAP_OFFSET,
                                                        CAP_REG_BYTE_SIZE,
                                                        AGAW_BIT_START),
                         "agaw",
                         "getIommuAGAW function not working")

        self.assertEqual(self.iommucreator.getIommuAGAW(IOMMUADDR,
                                                        testdevmem_invalid,
                                                        CAP_OFFSET,
                                                        CAP_REG_BYTE_SIZE,
                                                        AGAW_BIT_START),
                         "agaw",
                         "getIommuAGAW function not working")

    def test_IommuNamer(self):
        print "IommuDevicesCreatorTestCase:test_IommuNamer - begin"
        # Tests IommuNamer class in IommuDevicesCreator
        iommuaddrlist = ["addr1", "addr2", "addr3", "addr4"]
        iommunamer1 = creator.IommuDevicesCreator.IommuNamer(iommuaddrlist)
        self.assertEqual(
            iommunamer1.getName(), "iommu_1", "IommuNamer class not working")
        self.assertEqual(
            iommunamer1.getName(), "iommu_2", "IommuNamer class not working")
        self.assertEqual(
            iommunamer1.getName(), "iommu_3", "IommuNamer class not working")
        self.assertEqual(
            iommunamer1.getName(), "iommu_4", "IommuNamer class not working")

        iommuaddrlist2 = ["addr1"]
        iommunamer2 = creator.IommuDevicesCreator.IommuNamer(iommuaddrlist2)
        self.assertEqual(
            iommunamer2.getName(), "iommu", "IommuNamer class not working")

    def test_createDeviceFromAddr(self):
        print "IommuDevicesCreatorTestCase:test_IommuNamer - begin"
        DEVMEM = paths.DEVMEM
        CAPABILITY_OFFSET = "0x08"
        CAP_REG_BYTE_SIZE = 7
        AGAW_BIT_START = 8
        IOMMU_SIZE = "1000"

        iommuaddr = "0xfed91000"
        testiommuaddr = "0x0"
        devmemloc = os.path.join(self.testdir, "testdevmem")
        iommunamer = self.iommucreator.IommuNamer([testiommuaddr])

        iommudev = self.iommucreator.createDeviceFromAddr(devmemloc,
                                                          testiommuaddr,
                                                          iommunamer,
                                                          IOMMU_SIZE,
                                                          CAPABILITY_OFFSET,
                                                          CAP_REG_BYTE_SIZE,
                                                          AGAW_BIT_START)

        device = Element("device", "deviceType")

        # name attr
        device["name"] = "iommu"

        # memory
        memory = Element("memory", "deviceMemoryType")
        memory["caching"] = "UC"  # TODO
        memory["name"] = "mmio"
        memory["physicalAddress"] = "16#0000#"
        memory["size"] = "16#1000#"
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
        agawcap.content = "39"
        capabilities.appendChild(agawcap)
        device.appendChild(capabilities)

        self.assertEqual(
            iommudev.isEqual(device), True, "createDeviceFromAddr not working")

# == Tests schemadata.py ==
from src import schemadata
from src.schemadata import Element
import schemadata.testschema as schema
import copy


class SchemaDataTestCase(unittest.TestCase):

    "Tests the schemadata file"

    def setUp(self):
        print "<> SchemaDataTestCase:setUp - begin"
        self.testdir = testpaths.PATH_TEST_SCHEMADATA

    def tearDown(self):
        print "<> SchemaDataTestCase:tearDown - begin"

    # - Element class testcases
    def test_Element_toXML(self):
        "Tests the toXML function"
        print "SchemaDataTestCase:test_Element_toXML - begin"

        processor = Element("processor", "processorType")
        processor["logicalCpus", "speed", "vmxTimerRate"] = 1, 2, 3

        testxml = """<?xml version="1.0" encoding="utf-8"?><processor logicalCpus="1" speed="2" vmxTimerRate="3"/>"""
        self.assertEqual(
            processor.toXML("utf-8"), testxml, "toXML function not working")

    def test_Element_SetAttribute(self):
        "Tests the validity of setting attributes"
        print "SchemaDataTestCase:test_Element_SetAttribute - begin"

        processor = Element("processor", "processorType")
        processor["logicalCpus"] = 10
        processor["speed"] = 15
        processor["vmxTimerRate"] = [20]

        # Test for setting of invalid attribute of processorType
        self.assertRaises(
            customExceptions.InvalidAttribute, processor.__setitem__, "price", 100)

        # Test for permanence of attribute setting when converted to binding
        # Pyxb object
        processor_pyxb = processor.compileToPyxb()
        self.assertEqual(
            processor_pyxb.logicalCpus, 10, "Attribute setting failed")
        self.assertEqual(processor_pyxb.speed, 15, "Attribute setting failed")

        # Test for correctly not setting empty attributes
        devices = Element("devices", "devicesType")
        devices["pciConfigAddress"] = ""
        devices.compileToPyxb()

        # Test for setting multiple attributes
        processor["logicalCpus", "speed", "vmxTimerRate"] = 1, 2, 3
        processor_pyxb = processor.compileToPyxb()
        self.assertEqual(
            processor_pyxb.logicalCpus, 1, "Multiple attribute setting failed")
        self.assertEqual(
            processor_pyxb.speed, 2, "Multiple attribute setting failed")
        self.assertEqual(
            processor_pyxb.vmxTimerRate, 3, "Multiple attribute setting failed")

        self.assertRaises(customExceptions.AttributeMismatch,
                          processor.__setitem__, ["logicalCpus", "speed"], [1, 2, 3])
        self.assertRaises(customExceptions.InvalidAttribute,
                          processor.__setitem__, ["logicalCpus", "price", "speed"], [1, 2, 3])

    def test_Element_SetContent(self):
        "Tests the validity of setting element content"
        print "SchemaDataTestCase:test_Element_SetContent - begin"
        capability = Element("capability", "capabilityType")
        capability.setContent("Content1")
        capability["name"] = "content1"
        testXML = """<?xml version="1.0" encoding="utf-8"?><capability name="content1">Content1</capability>"""
        self.assertEqual(capability.toXML('utf-8'),
                         testXML, "setContent function not working")

    def test_Element_GetItem(self):
        "Tests the validity of retrieving attributes"
        print "SchemaDataTestCase:test_Element_GetItem - begin"

        processor = Element("processor", "processorType")
        processor["logicalCpus"] = 10
        processor["speed"] = 15
        processor["vmxTimerRate"] = [20]

        self.assertEqual(
            processor["logicalCpus"], 10, "Attribute Retrieving failed")
        self.assertRaises(
            customExceptions.InvalidAttribute, processor.__getitem__, "price")

    def test_Element_appendChild(self):
        "Tests the capability to add and remove child elements"
        print "SchemaDataTestCase:test_Element_appendChild - begin"

        memory = Element("memory", "physicalMemoryType")

        memoryBlock = Element("memoryBlock", "memoryBlockType")
        memoryBlock["physicalAddress", "size",
                    "name"] = "16#1111#", "16#2222#", "mem"

        memoryBlock2 = Element("memoryBlock", "memoryBlockType")
        memoryBlock2["physicalAddress", "size", "name",
                     "allocatable"] = "16#0101#", "16#0000#", "mem2", "true"

        memory.appendChild(memoryBlock)
        self.assertEqual(
            memoryBlock.getParent(), memory, "appendChild function not working")
        memory.removeChild(memoryBlock)

        memory.appendChild(memoryBlock)
        memory_pyxb = memory.compileToPyxb()
        self.assertEqual(memory_pyxb.memoryBlock[
                         0].size, "16#2222#", "appendChild function failed")

        memory.removeChild(memoryBlock)
        memory_pyxb = memory.compileToPyxb()
        self.assertRaises(IndexError, memory_pyxb.memoryBlock.__getitem__, 0)

        memory.appendChild(memoryBlock, memoryBlock2)
        memory_pyxb = memory.compileToPyxb()
        self.assertEqual(memory_pyxb.memoryBlock[
                         1].name, "mem2", "appendChild function failed")

        memory.appendChild([memoryBlock, memoryBlock2])
        memory_pyxb = memory.compileToPyxb()
        self.assertEqual(memory_pyxb.memoryBlock[
                         1].name, "mem2", "appendChild function failed")

        self.assertEqual(memory.appendChild(None),
                         False, "appendChild function not working")

    def test_Element_ListElements(self):
        "Tests the capabilities to include list elements"
        print "SchemaDataTestCase:test_Element_listElements - begin"

        memory = Element("memory", "physicalMemoryType")

        memoryBlock = Element("memoryBlock", "memoryBlockType")
        memoryBlock["physicalAddress", "size",
                    "name"] = "16#0000#", "16#4fff#", "mem1"

        memoryBlock2 = Element("memoryBlock", "memoryBlockType")
        memoryBlock2["physicalAddress", "size", "name",
                     "allocatable"] = "16#0101#", "16#0000#", "mem2", "true"

        memoryBlock3 = Element("memoryBlock2", "memoryBlockType")
        memoryBlock3["physicalAddress", "size",
                     "name"] = "16#abcd#", "16#1234#", "mem3"

        memory.appendChild(memoryBlock)
        memory.appendChild(memoryBlock2)
        memory.appendChild(memoryBlock3)

        memory_pyxb = memory.compileToPyxb()
        self.assertEqual(memory_pyxb.memoryBlock[
                         0].name, "mem1", "Nesting of list elements failed")
        self.assertEqual(memory_pyxb.memoryBlock[
                         1].physicalAddress, "16#0101#", "Nesting of list elements failed")

        testXML = """<?xml version="1.0" encoding="utf-8"?><memory><memoryBlock name="mem1" physicalAddress="16#0000#" size="16#4fff#"/>"""
        testXML += """<memoryBlock allocatable="true" name="mem2" physicalAddress="16#0101#" size="16#0000#"/></memory>"""

        self.assertEqual(memory.toXML("utf-8"), testXML,
                         "Compiling of list elements does not match expected output")

    def test_Element_NestedElements(self):
        "Tests the capabilities to have deep nested elements"
        print "SchemaDataTestCase:test_Element_NestedElements - begin"

        devices = Element("devices", "devicesType")
        devices["pciConfigAddress"] = "16#0000#"

        device1 = Element("device", "deviceType")
        device1["name"] = "Device1"

        device1_pci = Element("pci", "pciType")
        device1_pci["bus", "device", "function"] = "16#4f#", "16#0a#", 4
        device1.appendChild(device1_pci)

        device1_ioPort1 = Element("ioPort", "ioPortType")
        device1_ioPort1[
            "name", "start", "end"] = "device1_ioPort1", "16#0000#", "16#ffff#"
        device1_ioPort2 = Element("ioPort", "ioPortType")
        device1_ioPort2[
            "name", "start", "end"] = "device1_ioPort2", "16#1111#", "16#aaaa#"

        device1.appendChild(device1_ioPort1, device1_ioPort2)

        device1_capabilities = Element("capabilities", "capabilitiesType")
        device1.appendChild(device1_capabilities)
        device1_capabilitytype1 = Element("capability", "capabilityType")
        device1_capabilitytype1["name"] = "Device1 Capability1"
        device1_capabilitytype2 = Element("capability", "capabilityType")
        device1_capabilitytype2["name"] = "Device1 Capability2"
        device1_capabilities.appendChild(
            device1_capabilitytype1, device1_capabilitytype2)

        device2 = Element("device", "deviceType")
        device2["name"] = "Device2"

        device2_irq1 = Element("irq", "irqType")
        device2_irq1["name", "number"] = "device2_irq1", "100"
        device2_irq2 = Element("irq", "irqType")
        device2_irq2["name", "number"] = "device2_irq2", "200"
        device2.appendChild(device2_irq1, device2_irq2)
        device2_memory1 = Element("memory", "deviceMemoryType")
        device2_memory2 = Element("memory", "deviceMemoryType")
        device2.appendChild(device2_memory1, device2_memory2)
        device2_memory1["name", "physicalAddress", "size",
                        "caching"] = "device2_memory1", "16#0000#", "16#1111#", "UC"
        device2_memory2["name", "physicalAddress", "size",
                        "caching"] = "device2_memory2", "16#3333#", "16#4444#", "WC"

        devices.appendChild(device1, device2)
        devices_pyxb = devices.compileToPyxb()

        self.assertEqual(devices_pyxb.device[1].irq[
                         1].name, "device2_irq2", "Deep nesting of elements failed")
        self.assertEqual(devices_pyxb.device[0].capabilities.capability[
                         0].name, "Device1 Capability1", "Deep nesting of elements failed")

    def test_Element_isEqual(self):
        print "SchemaDataTestCase:test_Element_Compare - begin"

        # DEVICE_1
        device1 = Element("device", "deviceType")
        # name attr
        device1["name"] = "dev"
        # memory
        memory = Element("memory", "deviceMemoryType")
        memory["caching"] = "UC"
        memory["name"] = "mmio"
        memory["physicalAddress"] = "addr"
        memory["size"] = "size"
        device1.appendChild(memory)
        # capabilities
        capabilities = Element("capabilities", "capabilitiesType")
        # iommu
        iommucap1 = Element("capability", "capabilityType")
        iommucap1["name"] = "iommu"
        capabilities.appendChild(iommucap1)
        # agaw
        agawcap = Element("capability", "capabilityType")
        agawcap["name"] = "agaw"
        agawcap.content = "39"
        capabilities.appendChild(agawcap)
        device1.appendChild(capabilities)

        # DEVICE_2
        device2 = Element("device", "deviceType")
        # name attr
        device2["name"] = "dev"
        # memory
        memory = Element("memory", "deviceMemoryType")
        memory["caching"] = "UC"
        memory["name"] = "mmio"
        memory["physicalAddress"] = "addr"
        memory["size"] = "size"
        device2.appendChild(memory)
        # capabilities
        capabilities = Element("capabilities", "capabilitiesType")
        # iommu
        iommucap2 = Element("capability", "capabilityType")
        iommucap2["name"] = "iommu"
        capabilities.appendChild(iommucap2)
        # agaw
        agawcap = Element("capability", "capabilityType")
        agawcap["name"] = "agaw"
        agawcap.content = "39"
        capabilities.appendChild(agawcap)
        device2.appendChild(capabilities)

        dict1 = {
            "k1": "value1",
            "k2": "value2"
        }
        dict2 = {
            "k2": "value2",
            "k1": "value1"
        }

        cap_1 = Element("capabilities", "capabilitiesType")
        cap_2 = Element("capabilities", "capabilitiesType")

        cap_1.appendChild(iommucap1)
        cap_1.appendChild(iommucap2)
        cap_2.appendChild(iommucap2)

        self.assertEqual(dict1, dict2, "Dicts don't match")
        # Test attribute equals on one layer
        self.assertEqual(iommucap1.isEqual(iommucap2),
                         True, "Element isEqual function not working")

        # Test attribute equals on two layers
        self.assertEqual(
            cap_1.isEqual(cap_2), False, "Element isEqual function not working")
        mem1 = Element("memory", "physicalMemoryType")
        mem1_block1 = Element("memoryBlock", "memoryBlockType")
        mem1_block1[
            "name", "physicalAddress", "size", "allocatable"] = ("name",
                                                                 "addr",
                                                                 "size",
                                                                 "true")
        mem1_block2 = Element("memoryBlock", "memoryBlockType")
        mem1_block2[
            "name", "physicalAddress", "size", "allocatable"] = ("name",
                                                                 "addr",
                                                                 "size",
                                                                 "true")
        mem1.appendChild(mem1_block1, mem1_block2)

        mem2 = Element("memory", "physicalMemoryType")
        mem2_block1 = Element("memoryBlock", "memoryBlockType")
        mem2_block1[
            "name", "physicalAddress", "size", "allocatable"] = ("name",
                                                                 "addr",
                                                                 "size",
                                                                 "true")
        mem2_block2 = Element("memoryBlock", "memoryBlockType")
        mem2_block2[
            "name", "physicalAddress", "size", "allocatable"] = ("name",
                                                                 "addr",
                                                                 "size",
                                                                 "false")
        mem2.appendChild(mem2_block1, mem2_block2)

        self.assertEqual(
            mem1.isEqual(mem2), False, "Element isEqual function not working")
        mem2_block2["allocatable"] = "true"
        self.assertEqual(
            mem1.isEqual(mem2), True, "Element isEqual function not working")

        # Test content equals
        mem1_block2.content = "content"
        mem2_block2.content = "content2"

        self.assertEqual(
            mem1.isEqual(mem2), False, "Element isEqual function not working")
        mem2_block2.content = "content"
        self.assertEqual(
            mem1.isEqual(mem2), True, "Element isEqual function not working")

        self.assertEqual(device1.isEqual(device2),
                         True, "Element isEqual function not working")

    def createBindings_patch(x, y, z, a):
        return True

    def test_createBindings(self):
        testschema = os.path.join(self.testdir, "testschema.xsd")
        testschema_invalid = os.path.join(
            self.testdir, "testschema_invalid.file")
        outpath = testpaths.PATH_TEST_GEN
        # Normal function
        schemadata.createBindings(testschema,
                                  outpath,
                                  "testschemaoutput",
                                  paths.PYXB_GEN)

        # Invalid schema file chosen
        
        self.assertRaises(customExceptions.PyxbgenInvalidSchema,
                          schemadata.createBindings,
                          testschema_invalid,
                          outpath,
                          "testschemaoutput",
                          paths.PYXB_GEN)

        # No pyxb detected
        self.assertRaises(OSError,
                          schemadata.createBindings,
                          testschema,
                          outpath,
                          "testschemaoutput",
                          "invalidcommand")

    def test_copyEnvWithPythonPath(self):
        myenv = os.environ.copy()
        pythonpathstr = ""
        for pythonpath in sys.path:
            pythonpathstr = pythonpathstr + pythonpath + ":"
        myenv["PYTHONPATH"] = pythonpathstr
        self.assertEqual(schemadata.copyEnvWithPythonPath(),
                         myenv, "copyEnvWithPythonPath test failed")


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
        self.assertEqual(devicecap.translate("0x10"),
                         "PCI Express", "translate function not working")
        self.assertRaises(
            customExceptions.CapabilityUnknown, devicecap.translate, "0x0101")

    def test_DevicecapManager(self):
        "Tests the DevicecapManager class"
        print "DevicecapTestCase:test_DevicecapManager - begin"
        devicecapmgr = devicecap.DevicecapManager()

        # -- extractCapabilities function
        devloc = os.path.join(self.testdir, "devices")
        devpaths = []
        devpaths.append(os.path.join(devloc, "dev0"))
        devpaths.append(os.path.join(devloc, "pcibridge0"))
        devpaths = sorted(devpaths)
        devicecapmgr.extractCapabilities(devpaths)

        devicecapmgr.getCapList(os.path.join(devloc, "dev0"), False)
        devicecapmgr.getCapList(os.path.join(devloc, "pcibridge0"))
        devicecapmgr.getCapValue(os.path.join(devloc, "dev0"), "0x09")
        devicecapmgr.getCapValue(os.path.join(devloc, "pcibridge0"), "0x09")

        devpath_noaccess = os.path.join(devloc, "dev1_noaccess")
        self.assertRaises(customExceptions.DeviceCapabilitiesNotRead,
                          devicecapmgr.extractCapabilities,
                          [devpath_noaccess])

        # -- readCapFile function
        loc = os.path.join(testpaths.PATH_TEST_GEN, "testReadCapFile")
        with open(loc, "wb") as f:
                           # 00  01  02  03  04  05  06  07  08  09  0a  0b  0c
                           # 0d  0e  0f
            f.write(
                b"\x00\x01\x04\x03\x0a\x0e\x0c\x0a\x0e\x0c\x0d\x08\x0f\x00\x0b\x06")
        test_capcode1 = [
            cap.code for cap in devicecapmgr._readCapFile(loc, 0x02, 1, 1)]
        test_capcode2 = [
            cap.code for cap in devicecapmgr._readCapFile(loc, 0x02, 1, 1, 0x0, 3)]
        self.assertEqual(
            test_capcode1, ["0x0a", "0x0b", "0x0c", "0x0d", "0x0e", "0x0f"], "readCapFile function not working")
        self.assertEqual(
            test_capcode2, ["0x0a", "0x0b", "0x0c"], "readCapFile function not working")
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
        self.testdir = testpaths.PATH_TEST_UTIL

    def tearDown(self):
        print "<> UtilTestCase:tearDown - begin"

    def test_removeListsFromList(self):
        "Tests the removeListsFromList function"
        print "UtilTestCase:test_removeListsFromList - begin"
        mainList = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        removeList1 = [2, 4]
        removeList2 = [3, 7]
        removeList3 = [3, 6]
        removeList4 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        self.assertEqual(util.removeListsFromList(mainList, removeList1, removeList2), [
                         1, 5, 6, 8, 9, 10], "removeListsFromList function not working")
        self.assertEqual(util.removeListsFromList(mainList, removeList2, removeList3), [
                         1, 2, 4, 5, 8, 9, 10], "removeListsFromList function not working")
        self.assertEqual(util.removeListsFromList(mainList, removeList4),
                         [], "removeListsFromList function not working")
        
    def test_makefolder(self):
        print "UtilTestCase:test_makefolder - begin"

        tempfolder = os.path.join(self.testdir, "test_makefolder")
        if os.path.isdir(tempfolder):
            os.rmdir(tempfolder)
        util.makefolder(tempfolder)
        self.assertEqual(
            os.path.isdir(tempfolder), True, "makefolder failed")
        os.rmdir(tempfolder)
        os.mkdir(tempfolder)
        util.makefolder(tempfolder)  # see if fails when exists
        os.rmdir(tempfolder)

    def test_getBit(self):
        "Tests the getBit function"
        print "UtilTestCase:test_getBit - begin"
        self.assertEqual(util.getBit(5, 2), 1, "getBit function not working")
        self.assertEqual(util.getBit(5, 5), 0, "getBit function not working")

    def test_getLinks(self):
        "Tests the getLinks function"
        print "UtilTestCase:test_getLinks - begin"
        testdir = os.path.join(self.testdir, "test_getFilesInPath")

        def filterexp(filename):
            if filename.startswith("file"):
                return True
            else:
                return False

        testlist = ["doc1", "file0", "file1", "file2", "file3"]
        testfilteredlist = ["file0", "file1", "file2", "file3"]

        # Get the absolute location of symbolic links in path
        testnotfilteredpaths = []
        for filename in testlist:
            filePath = os.path.join(testdir, filename)
            relativeLink = os.readlink(filePath)
            absLink = os.path.join(os.path.dirname(filePath), relativeLink)
            testnotfilteredpaths.append(absLink)

        testfilteredpaths = []
        for filename in testfilteredlist:
            filePath = os.path.join(testdir, filename)
            relativeLink = os.readlink(filePath)
            absLink = os.path.join(os.path.dirname(filePath), relativeLink)
            testfilteredpaths.append(absLink)

        self.assertEqual(util.getLinks(testdir),
                         testnotfilteredpaths,
                         "getFilesInPath function not working")

        self.assertEqual(util.getLinks(testdir, filterexp),
                         testfilteredpaths,
                         "getFilesInPath function not working")

    def test_getSpeedValue(self):
        "Tests the getSpeedValue function"
        print "UtilTestCaseL:test_getSpeedValue - begin"
        validspeeds = ["GHz", "MHz"]
        self.assertEqual(util.getSpeedValue("3.20GHz", validspeeds),
                         3200, "getSpeedValue function not working")
        self.assertEqual(util.getSpeedValue("3.22GHz", validspeeds),
                         3220, "getSpeedValue function not working")
        self.assertEqual(util.getSpeedValue("800.0MHz", validspeeds),
                         800.0, "getSpeedValue function not working")
        self.assertEqual(util.getSpeedValue("800KHz", validspeeds),
                         None, "getSpeedValue function not working")
        self.assertEqual(util.getSpeedValue("0GHz", validspeeds),
                         0, "getSpeedValue function not working")
        self.assertEqual(util.getSpeedValue("GHz", validspeeds),
                         None, "getSpeedValue function not working")
        self.assertEqual(util.getSpeedValue("TenGHz", validspeeds),
                         None, "getSpeedValue function not working")
        self.assertEqual(util.getSpeedValue("2893.430 MHz.", validspeeds),
                         2893.43, "getSpeedValue not working with trailing dot")

    def test_numberMultiples(self):
        "Tests the numberMultiples function"
        print "UtilTestCase:test_numberMultiples - begin"
        testlist = ["elem", "elem", "elem2", "elem2", "elem3"]
        resultlist = ["elem_1", "elem_2", "elem2_1", "elem2_2", "elem3"]
        failedlist = ["elem_1", "elem2_1", "elem_2", "elem2_2", "elem3"]
        self.assertEqual(util.numberMultiples(testlist),
                         resultlist, "numberMultiples function not working")
        self.assertEqual(util.numberMultiples(
            []), [], "numberMultiples function not working")

    def test_ListNumberer(self):
        "Tests the ListNumberer class"
        print "UtilTestCase:test_ListNumberer - begin"
        testlist = ["elem", "elem", "elem2", "elem2", "elem3"]
        listnumberer = util.ListNumberer(testlist)
        self.assertEqual(listnumberer.getName("elem"),
                         "elem_1", "ListNumberer class not working")
        self.assertEqual(listnumberer.getName("elem"),
                         "elem_2", "ListNumberer class not working")
        self.assertEqual(listnumberer.getName("elem2"),
                         "elem2_1", "ListNumberer class not working")
        self.assertEqual(listnumberer.getName(
            "elem3"), "elem3", "ListNumberer class not working")
        self.assertRaises(ValueError, listnumberer.getName, "elem4")

    def test_isHex(self):
        "Tests the isHex function"
        print "UtilTestCase:test_isHex - begin"
        self.assertEqual(
            util.isHex("0x34Fa"), True, "isHex function not working")
        self.assertEqual(
            util.isHex("03Fa0x"), False, "isHex function not working")

    def test_stripvalue(self):
        "Tests the stripvalue function"
        print "UtilTestCase:test_stripvalue - begin"
        self.assertEqual(util.stripvalue("0x5123fa"),
                         "5123fa", "stripvalue function not working")
        self.assertEqual(
            util.stripvalue("100"), "100", "stripvalud function not working")

    def test_toWord64(self):
        "Tests the toWord64 function"
        print "UtilTestCase: test_toWord64 - begin"
        self.assertEqual(util.toWord64("0x5faFFaD"),
                         "16#05fa_FFaD#", "toWord64 function not working")
        self.assertEqual(
            util.toWord64("0x0"), "16#0000#", "toWord64 function not working")
        self.assertEqual(
            util.toWord64(""), "", "toWords64 function not working")

    def test_unwrapWord64(self):
        "Tests the unwrapWord64 function"
        print "UtilTestCase: test_unwrapWord64 - begin"
        self.assertEqual(util.unwrapWord64("16#0009_a000#"),
                         "0x9a000", "unwrapWord64 function not working")
        self.assertEqual(util.unwrapWord64("16#0000#"),
                         "0x0", "unwrapWord64 function not working")
        self.assertEqual(util.unwrapWord64("0x1234"),
                         "0x1234", "unwrapWord64 function not working")
        self.assertRaises(ValueError, util.unwrapWord64, "15#0009_a000#")

    def test_wrap16(self):
        "Tests the wrap16 function"
        print "UtilTestCase: test_wrap16 - begin"
        self.assertEqual(
            util.wrap16("1234"), "16#1234#", "wrap16 function not working")
        self.assertEqual(
            util.wrap16(""), "16##", "wrap16 function not working")

    def test_spacesToUnderscores(self):
        "Tests the spacesToUnderscores function"
        print "UtilTestCase: test_spacesToUnderscores - begin"
        self.assertEqual(util.spacesToUnderscores("asd def"),
                         "asd_def", "spacestoUnderscores function not working")

    def test_sizeOf(self):
        "Tests the sizeOf function"
        print "UtilTestCase: test_sizeOf - begin"
        self.assertEqual(
            util.sizeOf("0x0002", "0x0001"), "0x2", "sizeOf function not working")
        self.assertEqual(
            util.sizeOf("0xe000", "0xe07f"), "0x80", "sizeOf function not working")
        self.assertRaises(ValueError, util.sizeOf, "0x1000", 2)

    def test_hexFloor(self):
        "Tests the hexFloor function"
        print "UtilTestCase: test_hexFloor - begin"
        MINSIZE = "0x1000"
        self.assertEqual(util.hexFloor("0x10", MINSIZE),
                         MINSIZE, "hexFloor function not working")
        self.assertEqual(util.hexFloor("0x1000", MINSIZE),
                         "0x1000", "hexFloor function not working")
        self.assertEqual(util.hexFloor("0x10000", MINSIZE),
                         "0x10000", "hexFloor function not working")

    def test_hexRoundToMultiple(self):
        "Tests the hexRoundToMultiple function"
        print "UtilTestCase: test_hexRoundToMultiple - begin"
        self.assertEqual(util.hexRoundToMultiple("0x9d800", "0x1000"),
                         "0x9e000", "hexRoundToMultiple function not working")
        self.assertEqual(util.hexRoundToMultiple("0x9e000", "0x1000"),
                         "0x9e000", "hexRoundToMultiple function not working")
        self.assertEqual(
            util.hexRoundToMultiple("0x9d800", "0x1000", rounddown=True),
            "0x9d000", "hexRoundToMultiple function not working")


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

    def test_update(self):
        print "UpdateTestCase:test_update - begin"

        def updatePciIds_patch(url, location):
            return True

        def updatePciIds_patchfail(url, location):
            return False

        @mock.patch.object(update, "updatePciIds", updatePciIds_patch)
        def runtest():
            return update.update()

        @mock.patch.object(update, "updatePciIds", updatePciIds_patchfail)
        def runtest_fail():
            return update.update()

        self.assertEqual(runtest(), True, "update function not working")

        self.assertEqual(runtest_fail(), False, "update function not working")

    def test_updatePciIds(self):
        print "UpdateTestCase:test_updatePciIds - begin"
        INVALID_ADDR = "http://test"
        testfile = os.path.join(self.testdir, "test_pciids.ids")
        self.assertRaises(customExceptions.PciIdsInvalidLink,
                          update.updatePciIds,
                          INVALID_ADDR, testfile)
        update.updatePciIds(os.path.join(self.testdir, "test_newupdate.ids"),
                            testfile)

# == Class that tests message.py ==
from src import message


class MessageTestCase(unittest.TestCase):

    "Tests the message.py file"

    def setUp(self):
        "Setup code"
        print "<> MessageTestCase:setUp - begin"

    def tearDown(self):
        "Cleanup code"
        print "MessageTestCase:tearDown - begin"

    def test_reset(self):
        message.reset()
        self.assertEqual(
            len(message.messagequeue), 0, "Reset function not working")

    def test_addMessage(self):
        message.reset()
        message.addWarning("Warning1")
        message.addError("Error1", False)
        message.addError("Error1", False)
        message.addMessage("Message1")
        # Should not keep duplicate messages
        self.assertEqual(len(message.messagequeue),
                         3, "Message duplication handling failed")
        self.assertRaises(
            customExceptions.ForceQuit, message.addError, "QuitError")

    def test_printMessages(self):
        message.printMessages()

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
        self.assertEqual(parseutil.parseLine_Sep(
            data.splitlines()[4], "testKey4", ":"), "testValue4", "Value obtained from file " + loc + " is incorrect.")
        self.assertEqual(parseutil.parseLine_Sep(
            data.splitlines()[0], "testKey"), "testValue", "Value obtained from file " + loc + " is incorrect.")
        self.assertEqual(parseutil.parseLine_Sep(data.splitlines()[0], "testKey", [
                         ":", ",", ""]), "testValue", "Value obtained from file " + loc + "is incorrect.")

        loc = self.testdir + "testCpuInfo.txt"
        data = extractor.extractData(loc)
        self.assertEqual(parseutil.parseLine_Sep(
            data.splitlines()[8], "cache size", ":"), "8192 KB", "Value obtained from file " + loc + " is incorrect.")
        self.assertEqual(
            parseutil.parseLine_Sep(data.splitlines()[4], "model name", ":"),
            "Intel(R) Xeon(R) CPU E31230 @ 3.20GHz",
            "Value obtained from file " + loc + " is incorrect."
        )

    def test_parseLine_Sep_keyDoesNotExist(self):
        "Tests parseLine_Sep with nonexistent key"
        print "ParseUtilTestCase:test_parseLine_Sep_keyDoesNotExist - begin"

        loc = self.testdir + "testParseUtil.txt"
        data = extractor.extractData(loc)
        self.assertRaises(customExceptions.KeyNotFound,
                          parseutil.parseLine_Sep, data.splitlines()[0], "testKey2")
        self.assertRaises(customExceptions.KeyNotFound,
                          parseutil.parseLine_Sep, data.splitlines()[0], "testKey12")

        loc = self.testdir + "testCpuInfo.txt"
        data = extractor.extractData(loc)
        self.assertRaises(customExceptions.KeyNotFound,
                          parseutil.parseLine_Sep, data.splitlines()[0], "numprocessors")

    def test_parseLine_Sep_valueDoesNotExist(self):
        "Tests parseLine_Sep with nonexistent value"
        print "ParseUtilTestCase:test_parseLine_Sep_valueDoesNotExist - begin"

        loc = self.testdir + "testParseUtil.txt"
        data = extractor.extractData(loc)
        self.assertEqual(parseutil.parseLine_Sep(
            data.splitlines()[2], "testKey3"), "NO_VALUE", "Value obtained from file " + loc + " is incorrect.")
        self.assertEqual(parseutil.parseLine_Sep(
            data.splitlines()[5], "testKey5", ":"), "NO_VALUE", "Value obtained from file " + loc + " is incorrect.")

        loc = self.testdir + "testCpuInfo.txt"
        data = extractor.extractData(loc)
        self.assertEqual(parseutil.parseLine_Sep(
            data.splitlines()[24], "power management", ":"), "NO_VALUE", "Value obtained from file " + loc + " is incorrect.")

    def test_parseLine_Sep_sepDoesNotExist(self):
        "Tests parseLine_Sep when separator cannot be found"
        print "ParseUtilTestCase:test_parseLine_Sep_sepDoesNotExist - begin"

        loc = self.testdir + "testCpuInfo.txt"
        data = extractor.extractData(loc)
        self.assertEqual(parseutil.parseData_Sep(
            data.splitlines()[5], "stepping", ","), "NO_VALUE", "Value obtained from file " + loc + " is incorrect.")

        loc = self.testdir + "testParseUtil.txt"
        data = extractor.extractData(loc)
        self.assertEqual(parseutil.parseData_Sep(
            data.splitlines()[0], "testKey", ":"), "NO_VALUE", "Value obtained from file " + loc + " is incorrect.")

    # -- parseData_Sep tests
    def test_parseData_Sep(self):
        "Tests parseData_Sep normal function"
        print "ParseUtilTestCase:test_parseData_Sep - begin"
        loc = self.testdir + "testParseUtil.txt"
        data = extractor.extractData(loc)
        self.assertEqual(parseutil.parseData_Sep(data, "testKey4", ":"),
                         "testValue4", "Value obtained from file " + loc + " is incorrect.")
        self.assertEqual(parseutil.parseData_Sep(data, "testKey2"),
                         "testValue2 testValue2.1 testValue2.2", "Value obtained from file " + loc + " is incorrect.")

        loc = self.testdir + "testCpuInfo.txt"
        data = extractor.extractData(loc)
        self.assertEqual(parseutil.parseData_Sep(data, "cpu cores", ":"),
                         "4", "Value obtained from file " + loc + " is incorrect.")

    def test_parseData_Sep_keyNotFound(self):
        "Tests parseData_Sep with inexistent key"
        print "ParseUtilTestCase:test_parseData_Sep_keyNotFound - begin"
        loc = self.testdir + "testParseUtil.txt"
        data = extractor.extractData(loc)
        self.assertRaises(customExceptions.KeyNotFound,
                          parseutil.parseData_Sep, data, "testKeyNotExists")

        loc = self.testdir + "testCpuInfo.txt"
        data = extractor.extractData(loc)
        self.assertRaises(customExceptions.KeyNotFound,
                          parseutil.parseData_Sep, data, "testKeyNotExists")

    def test_parseData_Sep_valueDoesNotExist(self):
        "Tests parseData_Sep to obtain value that does not exist"
        print "ParseUtilTestCase:test_parseData_Sep_valueDoesNotExist - begin"
        loc = self.testdir + "testCpuInfo.txt"
        data = extractor.extractData(loc)
        self.assertEqual(
            parseutil.parseData_Sep(data, "power management", ":"),
            "NO_VALUE", "Value obtained from file " + loc + " is incorrect.")

    def test_parseData_Sep_sepDoesNotExist(self):
        "Tests parseData_Sep when separator cannot be found"
        print "ParseUtilTestCase:test_parseData_Sep_sepDoesNotExist - begin"
        loc = self.testdir + "testCpuInfo.txt"
        data = extractor.extractData(loc)
        self.assertEqual(parseutil.parseData_Sep(data, "stepping", ","),
                         "NO_VALUE", "Value obtained from file " + loc + " is incorrect.")

        loc = self.testdir + "testParseUtil.txt"
        data = extractor.extractData(loc)
        self.assertEqual(parseutil.parseData_Sep(data, "testKey", ":"),
                         "NO_VALUE", "Value obtained from file " + loc + " is incorrect.")

    # -- findLines tests
        "Tests findLines function"
        print "ParseUtilTestCase:test_findLines - begin"
        loc = self.testdir + "testParseUtil.txt"
        data = extractor.extractData(loc)
        self.assertEqual(parseutil.findLines(data, "testValue4")[
                         0], "testKey4 : testValue4", "findLine function not working")

    # -- count tests
    def test_count(self):
        "Tests count with normal function"
        print "ParseUtilTestCase:test_count - begin"
        loc = self.testdir + "testParseUtil.txt"
        data = extractor.extractData(loc)
        self.assertEqual(parseutil.count(data, "testCount"), 6,
                         "Value obtained from file " + loc + " is incorrect.")
        self.assertEqual(parseutil.count(data, "testCount3"), 2,
                         "Value obtained from file " + loc + " is incorrect.")

    def test_count_keyNotFound(self):
        "Tests count with nonexistent key"
        print "ParseUtilTestCase:test_count_keyNotFound - begin"
        loc = self.testdir + "testParseUtil.txt"
        data = extractor.extractData(loc)
        self.assertEqual(parseutil.count(data, "testCount4"), 0,
                         "Value obtained from file " + loc + " is incorrect.")

    # -- PciIdsParser tests
    def test_PciIdsParser(self):
        "Tests the PciIdsParser class"
        print "ParseUtilTestCase:test_PciIdsParser - begin"
        pciIdsLoc = testpaths.PATH_PCIIDS
        pciIdsLocMultiple = testpaths.PATH_TEST_PARSEUTIL + \
            "testpciids_multiple"
        pciIdsLocInit = testpaths.PATH_TEST_PARSEUTIL + "testpciids_init"
        parser = parseutil.PciIdsParser(pciIdsLoc)

        # isValidVendorCode function
        self.assertEqual(parser.isValidVendorCode("0000"),
                         True, "isValidVendorCode function not working")
        self.assertEqual(parser.isValidVendorCode("a0102"),
                         False, "isValidVendorCodefunction not working")
        self.assertEqual(parser.isValidVendorCode("#"),
                         False, "isValidVendorCode function not working")

        # isValidDeviceCode function
        self.assertEqual(parser.isValidDeviceCode("0000"),
                         True, "isValidDeviceCode function not working")
        self.assertEqual(parser.isValidDeviceCode("12"),
                         False, "isValidDeviceCodefunction not working")
        self.assertEqual(parser.isValidDeviceCode("#"),
                         False, "isValidDeviceCode function not working")
        self.assertEqual(parser.isValidDeviceCode("____"),
                         False, "isValidDeviceCode function not working")

        # isValidClassCode function
        self.assertEqual(parser.isValidClassCode("02"),
                         True, "isValidClassCode function not working")
        self.assertEqual(parser.isValidClassCode("0301"),
                         False, "isValidClassCodefunction not working")
        self.assertEqual(parser.isValidClassCode("#"),
                         False, "isValidClassCode function not working")

        # isValidSubclassCode function
        self.assertEqual(parser.isValidSubclassCode("01"),
                         True, "isValidSubclassCode function not working")
        self.assertEqual(parser.isValidSubclassCode("a12"),
                         False, "isValidSubclassCodefunction not working")
        self.assertEqual(parser.isValidSubclassCode("#"),
                         False, "isValidSubclassCode function not working")

        # isVendor function
        self.assertEqual(
            parser.isVendor("0a12  Vendor1"), True, "isVendor function not working")
        self.assertEqual(
            parser.isVendor("0a12  Vendor1, Inc."), True, "isVendor function not working")
        self.assertEqual(
            parser.isVendor("	0a12  Vendor2"), False, "isVendor function not working")

        # isDevice function
        self.assertEqual(
            parser.isDevice("	0101  Device1"), True, "isDevice function not working")
        self.assertEqual(
            parser.isDevice("      0203  Device1_spacenottab"), False, "isDevice function not working")
        self.assertEqual(
            parser.isDevice("		0232  Device1"), False, "isDevice function not working")

        # isClass function
        self.assertEqual(
            parser.isClass("C 01  Class1"), True, "isClass function not working")
        self.assertEqual(
            parser.isClass("0a12 Vendor1"), False, "isClass function not working")

        # isSubclass function
        self.assertEqual(
            parser.isSubclass("	02  Subclass1"), True, "isSubclass function not working")
        self.assertEqual(parser.isSubclass("		02  Subsubclass"),
                         False, "isSubclass function not working")

        # init function
        parser_init = parseutil.PciIdsParser(pciIdsLocInit)
        self.assertEqual(len(parser_init.vendorData),
                         6, "PciIdsParser not initialised properly")
        self.assertEqual(len(parser_init.deviceData),
                         3, "PciIdsParser not initialised properly")
        self.assertEqual(len(parser_init.classData),
                         10, "PciIdsParser not initialised properly")

        self.assertRaises(
            customExceptions.PciIdsMultipleEntries, parseutil.PciIdsParser, pciIdsLocMultiple)

        # getVendorName function
        self.assertEqual(parser.getVendorName("0x0e11"),
                         "Compaq Computer Corporation", "getVendorName function not working")
        self.assertRaises(
            customExceptions.PciIdsFailedSearch, parser.getVendorName, "0x0400")

        # getDeviceName function
        self.assertEqual(parser.getDeviceName("0x0675", "0x1700"),
                         "IS64PH ISDN Adapter", "getDeviceName function not working")
        self.assertEqual(parser.getDeviceName("0x0675", "0x1704"),
                         "ISDN Adapter (PCI Bus, D, C)", "getDeviceName function not working")
        self.assertEqual(parser.getDeviceName("0x8086", "0x0108"),
                         "Xeon E3-1200 Processor Family DRAM Controller", "getDeviceName function not working")
        self.assertRaises(
            customExceptions.PciIdsFailedSearch, parser.getDeviceName, "0x0675", "0x2000")

        # getClassName function
        self.assertEqual(parser.getClassName("0x0604"),
                         "PCI bridge", "getClassName function not working")
        self.assertEqual(parser.getClassName("0x0c06"),
                         "InfiniBand", "getClassName function not working")
        self.assertEqual(parser.getClassName("0x0608"),
                         "RACEway bridge", "getClassName function not working")
        self.assertEqual(parser.getClassName("0x0600"),
                         "Host bridge", "getClassName function not working")
        self.assertRaises(
            customExceptions.PciIdsSubclassNotFound, parser.getClassName, "0x0685")
        self.assertRaises(
            customExceptions.PciIdsFailedSearch, parser.getClassName, "0x1400")


class DMARParserTestCase(unittest.TestCase):

    "Tests the DMARParser Class in parseutil"

    def setUp(self):
        "Setup code"
        print "<> DMARParserTestCase:setUp - begin"
        self.testdir = os.path.join(testpaths.PATH_TEST_PARSEUTIL)
        self.dmarparser = parseutil.DMARParser()
        # TO MOVE TO PARSEUTIL FOLDER

    def tearDown(self):
        "Cleanup code"
        print "DMARParserTestCase:tearDown - begin"

    def test_genDMAR_copyDMAR(self):
        print "DMARParserTestCase:test_genDMAR_copyDMAR - begin"
        dmarloc = os.path.join(self.testdir, "testdmar.dat")
        dmarloc_invalid = os.path.join(self.testdir, "testdmar_invalidloc.dat")
        dest = os.path.join(self.testdir, "testdmar_copy.dat")
        dest_invalid = ""

        self.assertEqual(
            self.dmarparser._genDMAR_copyDMAR(dmarloc_invalid, dest),
            False,
            "_genDMAR_copyDMAR function not working")

        self.assertEqual(
            self.dmarparser._genDMAR_copyDMAR(dmarloc, dest_invalid),
            False,
            "_genDMAR_copyDMAR function not working")

        self.assertEqual(self.dmarparser._genDMAR_copyDMAR(dmarloc, dest),
                         True,
                         "_genDMAR_copyDMAR function not working")

        self.assertEqual(self.dmarparser.getCopiedDmarPath(),
                         dest,
                         "_genDMAR_copyDMAR function not working")

    def test_parseDMAR(self):
        print "DMARParserTestCase:test_parseDMAR - begin"
        dmarloc = os.path.join(self.testdir, "testdmar_parseDMAR.dat")
        output = os.path.join(self.testdir, "testdmar_parseDMAR.dsl")

        # Mock success iasl
        def _runIasl_success(self, dmarloc):
            return True

        def _getCopiedDmarPath(self):
            return dmarloc

        def _runIasl_nocmd(self, dmarloc):
            subprocess.check_call("parseDMAR_nosuchcommand")

        def _runIasl_noinput(self, dmarloc):
            raise subprocess.CalledProcessError(255, "cmd", None)

        # Define functions with patched objects
        @mock.patch.object(parseutil.DMARParser, "_runIasl", _runIasl_success)
        @mock.patch.object(parseutil.DMARParser, "getCopiedDmarPath", _getCopiedDmarPath)
        def test_success(dmarloc):
            dmarparser = parseutil.DMARParser()
            return (dmarparser.parseDMAR(), dmarparser.getParsedDmarPath())

        @mock.patch.object(parseutil.DMARParser, "_runIasl", _runIasl_nocmd)
        def test_noiasl(dmarloc):
            dmarparser = parseutil.DMARParser()
            return dmarparser.parseDMAR(dmarloc)

        @mock.patch.object(parseutil.DMARParser, "_runIasl", _runIasl_noinput)
        def test_noinput(dmarloc):
            dmarparser = parseutil.DMARParser()
            return dmarparser.parseDMAR(dmarloc)

        self.assertEqual(test_success(dmarloc)[0],
                         True,
                         "parseDMAR function not working")
        self.assertEqual(test_success(dmarloc)[1],
                         output,
                         "parseDMAR function not working")
        self.assertEqual(test_noiasl(dmarloc),
                         False,
                         "parseDMAR function not working")
        self.assertRaises(subprocess.CalledProcessError,
                          test_noinput,
                          dmarloc)

    def test_genDMAR(self):
        print "DMARParserTestCase:test_genDMAR - begin"
        dmarloc = os.path.join(self.testdir, "testdmar.dat")
        outputfolder = os.path.join(self.testdir, "test_gendmar")
        destname = "test_gendmar.dat"
        outputloc = os.path.join(outputfolder, destname)

        self.dmarparser.genDMAR(dmarloc, outputloc)

        if os.path.isdir(outputfolder):
            shutil.rmtree(outputfolder)

    def test_getIommuAddrs(self):
        print "DMARParserTestCase:test_getIommuAddrs - begin"
        loc = os.path.join(self.testdir, "testdmar.dsl")
        emptyloc = os.path.join(self.testdir, "testdmar_empty.dsl")
        invalidloc = "get_IommuAddrs_invalidloc"

        correctdmarparser = parseutil.DMARParser()
        correctdmarparser.parsedDMAR = loc

        self.assertEqual(correctdmarparser.getIommuAddrs(),
                         ["0xfed91000", "0xfed91100"],
                         "getIommuAddrs function not working")
        self.assertEqual(self.dmarparser.getIommuAddrs(emptyloc),
                         [],
                         "getIommuAddrs function not working")
        self.assertEqual(self.dmarparser.getIommuAddrs(invalidloc),
                         [],
                         "getIommuAddrs function not working")


if not os.path.isdir(testpaths.PATH_TEST_GEN):
    os.mkdir(testpaths.PATH_TEST_GEN)

def unittest_cleanup():
        # Remove temp folders
        if os.path.isdir(paths.TEMP):
            shutil.rmtree(paths.TEMP)

        if os.path.isdir(testpaths.PATH_TEST_GEN):
            shutil.rmtree(testpaths.PATH_TEST_GEN)

if __name__ == "__main__":
    import atexit
    atexit.register(unittest_cleanup)
    unittest.main()
