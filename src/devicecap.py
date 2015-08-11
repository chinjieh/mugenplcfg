#Module to handle device capabilities
#From setpci --dumpreg command and Linux/include/uapi/linux/pci_regs.h
#This list can be appended when more capability IDs are found
import extractor
import os
import customExceptions
import util
import struct
from collections import namedtuple


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

translated = {	CAP_PM : "Power Management",
		CAP_AGP: "Accelerated Graphics Port",
		CAP_VPD: "Vital Product Data",
		CAP_SLOTID : "Slot Identification",
		CAP_MSI : "Message Signalled Interrupts" ,
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


class DevicecapManager():
	"Class that handles PCI device capability data"
	def __init__(self):
		self.capabilities = {}
			
	def extractCapabilities(self,devicepaths):
		"Checks if device capabilities can be found and creates capability dict"
		capabilities = {}
		#Initialise empty dictionary
		for devicepath in devicepaths:
			capabilities[devicepath] = []

		#Attempt to fill dictionary
		try:
			for devicepath in devicepaths:
				capabilities[devicepath] = self._extractCapability(devicepath)
		except customExceptions.NoAccessToFile:
			message.addError("Not enough permissions to access capabilities of "
							 "devices. It is advised to run the tool again with "
							 "the proper permissions.", False)
		self.capabilities = capabilities

	def _extractCapability(self, devicepath):
		"Gets capability for device"
		CAPABILITY_START = 0x34
		STATUS_REG_LOCATION = 0x6
		CAPABILITY_BIT_POS = 4
		NEXT_OFFSET = 1
		DATA_SIZE = 1
		STOP_ID = 0x00
		CAPABILITY_NUM = 48
		CONFIG_PATH = os.path.join(devicepath, "config")
	
		#Checks config file whether capability bit is activated
		capbyte = extractor.extractBinaryData(CONFIG_PATH, STATUS_REG_LOCATION, 1)
		capint = int(capbyte, 16)
		if util.getBit(capint, CAPABILITY_BIT_POS):
			#Checks config file, starting at CAPABILITY_START and moving through linked list
			return self._readCapFile(CONFIG_PATH,
									 CAPABILITY_START,
									 DATA_SIZE,
									 NEXT_OFFSET,
									 STOP_ID,
									 CAPABILITY_NUM)
		else:
			return []
		
	def getCap(self, devicepath, simple=True):
		result = None
		if simple:
			result = self.capabilities.get(devicepath)
			
		return result
	
	def _readCapFile(self, file, startpos, datasize, nextoffset=1, stopid=0x00, numJumps=-1):
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
			nextaddr = readdata(f, datasize)
			while (nextaddr != stopid and numJumps != 0):
				f.seek(nextaddr)
				data = readdata(f,datasize) #read data
				result.append("0x{:02x}".format(data))
				f.seek(nextoffset-1, 1) #move pointer to next
				nextaddr = readdata(f,datasize) #read next address
				numJumps -= 1
		return result


def translate(capcode):
	try:
		return translated[capcode]
	except KeyError:
		raise customExceptions.CapabilityUnknown(
			"Capability Code %s is unknown." % capcode )
		return capcode