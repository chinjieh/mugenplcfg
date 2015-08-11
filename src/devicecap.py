#Module to handle device capabilities
#From setpci --dumpreg command and Linux/include/uapi/linux/pci_regs.h
#This list can be appended when more capability IDs are found
import extractor
import os
import customExceptions
import util
import struct
from collections import namedtuple

Cap = namedtuple("Cap", "code , value")

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
	CAP_PM : "Power Management",
	CAP_AGP: "Accelerated Graphics Port",
	CAP_VPD: "Vital Product Data",
	CAP_SLOTID : "Slot Identification",
	CAP_MSI : "Message Signalled Interrupts",
	CAP_CHSWP : "CompactPCI Hotswap",
	CAP_PCIX : "PCI-X",
	CAP_HT : "HyperTransport",
	CAP_VNDR : "Vendor-Specific",
	CAP_DBG : "Debug Port" ,
	CAP_CCRC : "CompactPCI Central Resource Control" ,
	CAP_HOTPLUG : "PCI Standard Hot-Plug Controller",
	CAP_SSVID : "Bridge subsystem vendor/device ID",
	CAP_AGP3 : "AGP Target PCI-PCI bridge",
	CAP_SECURE : "Secure Device",
	CAP_EXP : "PCI Express",
	CAP_MSIX : "MSI-X",
	CAP_SATA : "SATA Data/Index Configuration",
	CAP_AF : "PCI Advanced Features"
	}

# CAPABILITY VALUES
CAP_MSI_VALUE = namedtuple("MSI", "enable")
CAP_MSIX_VALUE = namedtuple("MSIX", "enable")

class DevicecapManager():
	"Class that handles PCI device capability data"
	def __init__(self):
		self.capabilities = {} #devicepath, caplist

	def extractCapabilities(self,devicepaths):
		"Checks if device capabilities can be found and creates capability dict"
		#Attempt to fill dictionary
		try:
			for devicepath in devicepaths:
				self._extractCapability(devicepath, "config")
		except customExceptions.NoAccessToFile:
			message.addError("Not enough permissions to access capabilities of "
							 "devices. It is advised to run the tool again with "
							 "the proper permissions.", False)

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
	
		#Checks config file whether capability bit is activated
		capbyte = extractor.extractBinaryData(CONFIG_PATH, STATUS_REG_LOCATION, 1)
		capint = int(capbyte, 16)
		if util.getBit(capint, CAPABILITY_BIT_POS):
			#Checks config file, starting at CAPABILITY_START and moving through linked list
			self.capabilities[devicepath] = self._readCapFile(CONFIG_PATH,
															  CAPABILITY_START,
															  CAP_SIZE,
															  NEXT_OFFSET,
															  STOP_ID,
															  CAPABILITY_NUM)

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
		"Returns CapValue object for a device"
		result = None
		caplist = self.capabilities.get(devicepath)
		if caplist is not None:
			for cap in caplist:
				if cap.code == capcode:
					return cap.value
		return result
	
	def _readCapFile(self, file, startpos, capsize, nextoffset=1, stopid=0x00, numJumps=-1):
		"Extracts data from the config file that is in linked list format i.e "
		"reads address from startpos, reads data in address, reads address from "
		"ptroffset..."
		result = []
	
		def readdata(f,size):
			data = f.read(size)
			if data != "":
				#returns integer of data
				return struct.unpack('B', data)[0]
			else:
				raise customExceptions.NoAccessToFile(
					"No permission to read file: %s" % file )
	
		with open(file, "rb") as f:
			f.seek(startpos)
			nextaddr = readdata(f, capsize)
			while (nextaddr != stopid and numJumps != 0):
				f.seek(nextaddr)
				data = readdata(f,capsize) #read data - capcode
				capcode = "0x{:02x}".format(data)
				nextaddr = readdata(f,capsize) #read next address
				capvalue = self._getCapValue(capcode, f) #read cap info
				cap = Cap(code=capcode, value=capvalue)
				result.append(cap)
				numJumps -= 1
		return result
	
	def _getCapValue(self, capcode, fileobj):
		"Gets the extra information for capabilities in form of tuple"
		"Returns None if no Value found"
		
		def get_cap_msi():
			byte = struct.unpack('B',fileobj.read(1))[0]
			enablebit = util.getBit(byte, 0) #Last bit
			value = CAP_MSI_VALUE(enable=enablebit)
			return value
		
		def get_cap_msix():
			byte = struct.unpack('B',fileobj.read(1))[0]
			enablebit = util.getBit(byte,0) #Last bit
			value = CAP_MSIX_VALUE(enable=enablebit)
			return value
		
		switch = {
			CAP_MSI : get_cap_msi,
			CAP_MSIX : get_cap_msix
		}

		result = lambda : None
		try:
			result = switch[capcode]
		except KeyError:
			pass
		return result() #Perform function based on capcode


def translate(capcode):
	try:
		return translated[capcode]
	except KeyError:
		raise customExceptions.CapabilityUnknown(
			"Capability Code %s is unknown." % capcode )
		return capcode