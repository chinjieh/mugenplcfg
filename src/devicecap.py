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


# Module to handle device capabilities
# From setpci --dumpreg command and Linux/include/uapi/linux/pci_regs.h
# This list can be appended when more capability IDs are found
import extractor
import os
import customExceptions
import util
import struct
import message
from collections import namedtuple

# CAPABILITY CODES
CAP_PM = "0x01"
CAP_AGP = "0x02"
CAP_VPD = "0x03"
CAP_SLOTID = "0x04"
CAP_MSI = "0x05"
CAP_CHSWP = "0x06"
CAP_PCIX = "0x07"
CAP_HT = "0x08"
CAP_VNDR = "0x09"
CAP_DBG = "0x0a"
CAP_CCRC = "0x0b"
CAP_HOTPLUG = "0x0c"
CAP_SSVID = "0x0d"
CAP_AGP3 = "0x0e"
CAP_SECURE = "0x0f"
CAP_EXP = "0x10"
CAP_MSIX = "0x11"
CAP_SATA = "0x12"
CAP_AF = "0x13"

translated = {
    CAP_PM: "Power Management",
    CAP_AGP: "Accelerated Graphics Port",
    CAP_VPD: "Vital Product Data",
    CAP_SLOTID: "Slot Identification",
    CAP_MSI: "Message Signalled Interrupts",
    CAP_CHSWP: "CompactPCI Hotswap",
    CAP_PCIX: "PCI-X",
    CAP_HT: "HyperTransport",
    CAP_VNDR: "Vendor-Specific",
    CAP_DBG: "Debug Port",
    CAP_CCRC: "CompactPCI Central Resource Control",
    CAP_HOTPLUG: "PCI Standard Hot-Plug Controller",
    CAP_SSVID: "Bridge subsystem vendor/device ID",
    CAP_AGP3: "AGP Target PCI-PCI bridge",
    CAP_SECURE: "Secure Device",
    CAP_EXP: "PCI Express",
    CAP_MSIX: "MSI-X",
    CAP_SATA: "SATA Data/Index Configuration",
    CAP_AF: "PCI Advanced Features"
}


Cap = namedtuple("Cap", ["code", "value"])

# CAPABILITY VALUES (CapValue objects)
CAP_MSI_VALUE = namedtuple("MSI", "enable")
CAP_MSIX_VALUE = namedtuple("MSIX", "enable")

# CAPABILITY VALUE ACTIONS (on data after nextpointer)


def get_cap_msi(fileobj):
    byte = struct.unpack('B', fileobj.read(1))[0]
    enablebit = util.getBit(byte, 0)  # Last bit
    value = CAP_MSI_VALUE(enable=enablebit)
    return value


def get_cap_msix(fileobj):
    byte = struct.unpack('B', fileobj.read(1))[0]
    enablebit = util.getBit(byte, 0)  # Last bit
    value = CAP_MSIX_VALUE(enable=enablebit)
    return value

capswitcher = {
    CAP_MSI: get_cap_msi,
    CAP_MSIX: get_cap_msix
}


class DevicecapManager():

    "Class that handles PCI device capability data"

    def __init__(self):
        self.capabilities = {}  # devicepath, caplist

    def extractCapabilities(self, devicepaths):
        "Checks if device capabilities can be found and creates capability dict"
        # Call this function first to attempt to fill dictionary
        for devicepath in devicepaths:
            try:
                self._extractCapability(devicepath, "config")
            except (customExceptions.NoAccessToFile, IOError):
                raise customExceptions.DeviceCapabilitiesNotRead(
                    "Could not read capability: %s" % devicepath)

    def getCapList(self, devicepath, simple=True):
        "Returns list of capabilities, only codes if simple=True"
        result = []
        caplist = self.capabilities.get(devicepath)
        if caplist is not None:
            result = []
            if simple:
                for cap in caplist:
                    result.append(cap.code)
            else:
                result = caplist
        return result

    def getCapValue(self, devicepath, capcode):
        "Returns CapValue tuple for a device (additional information on capability)"
        result = None
        caplist = self.capabilities.get(devicepath)
        if caplist is not None:
            for cap in caplist:
                if cap.code == capcode:
                    return cap.value
        return result

    def getCapabilities(self):
        return self.capabilities

    def _extractCapability(self, devicepath, configfilename):
        "Gets capability for device"
        CAPABILITY_START = 0x34
        STATUS_REG_LOCATION = 0x6
        CAPABILITY_BIT_POS = 4
        NEXT_OFFSET = 1
        CAP_SIZE = 1
        STOP_ID = 0x00
        CAPABILITY_NUM = 48
        CONFIG_PATH = os.path.join(devicepath, configfilename)

        # Checks config file whether capability bit is activated
        capbyte = extractor.extractBinaryData(
            CONFIG_PATH, STATUS_REG_LOCATION, 1)
        capint = int(capbyte, 16)
        if util.getBit(capint, CAPABILITY_BIT_POS):
            # Checks config file, starting at CAPABILITY_START and moving
            # through linked list
            self.capabilities[devicepath] = self._readCapFile(CONFIG_PATH,
                                                              CAPABILITY_START,
                                                              CAP_SIZE,
                                                              NEXT_OFFSET,
                                                              STOP_ID,
                                                              CAPABILITY_NUM)

    def _readCapFile(self, file, startpos, capsize, nextoffset=1, stopid=0x00, numJumps=-1):
        """
        Extracts data from the config file that is in linked list format i.e
        reads address from startpos, reads data in address, reads address from
        ptroffset..."""
        result = []
        print "Reading device data : ", file

        def readdata(f, size):
            data = f.read(size)
            if data != "":
                # returns integer of data
                return struct.unpack('B', data)[0]
            else:
                raise customExceptions.NoAccessToFile(
                    "No permission to read file: %s" % file)

        with open(file, "rb") as f:
            f.seek(startpos)
            nextaddr = readdata(f, capsize)
            while (nextaddr != stopid and numJumps != 0):
                f.seek(nextaddr)
                data = readdata(f, capsize)  # read data - capcode
                capcode = "0x{:02x}".format(data)
                nextaddr = readdata(f, capsize)  # read next address
                capvalue = self._getCapValue(capcode, f)  # read cap info
                cap = Cap(code=capcode, value=capvalue)
                result.append(cap)
                numJumps -= 1
        return result

    def _getCapValue(self, capcode, fileobj):
        """Gets the extra information for capabilities in form of tuple.
        Returns None if no Value found."""
        result = lambda x: None
        try:
            result = capswitcher[capcode]
        except KeyError:
            pass
        return result(fileobj)  # Perform function based on capcode


def translate(capcode):
    try:
        return translated[capcode]
    except KeyError:
        raise customExceptions.CapabilityUnknown(
            "Capability Code %s is unknown." % capcode)
