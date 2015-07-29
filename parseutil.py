#Module containing utilities for parsing data
import util
import extractor
import customExceptions

class PciIdsParser():
	"Class used to parse pci.ids file"
	def __init__(self, pciIdsLoc):
		#initialise personal dictionary to decode vendor and device codes
		self.vendorData = {} #vencode = venname
		self.deviceData = {} #(vencode, devcode) = devname
		self.init(pciIdsLoc)
	
	def isValidCode(self,code):
		if len(code) is not 4:
			return False
		if code.isalnum() is False:
			return False
		return True

	def isVendor(self,line):
		if self.isValidCode(line.partition("  ")[0]):
			return True
		else: 
			return False

	def isDevice(self,line):
		result = False
		if self.isVendor(line) is False:
			if line.startswith("\t") :
				if line.count("\t") is 1:
					if self.isValidCode(line.partition("  ")[0].lstrip()) is True:
				 		result = True				
		return result

	def init(self,pciIdsLoc):
		"Fills up database from pci.ids at pciIdsLoc"
		try:
			data = extractor.extractData(pciIdsLoc)
			lastVendor = ""
			for line in data.splitlines():
				#find Vendor
				if self.isVendor(line):
					tokens = line.partition("  ")
					vendorcode = tokens[0].strip()
				
					if vendorcode not in self.vendorData:
						self.vendorData[vendorcode] = tokens[2].strip()
						lastVendor = vendorcode
					else:
						self.vendorData[vendorcode] = tokens[2].strip()
						lastVendor = vendorcode
						raise customExceptions.PciIdsMultipleEntries("Multiple instances of vendor with the same id detected")

				#if find Device, refer to last Vendor
				if self.isDevice(line):
					tokens = line.lstrip("\t").partition("  ")
					devicecode = tokens[0].strip()
					if (lastVendor, devicecode) not in self.deviceData:
						self.deviceData[(lastVendor, devicecode)] = tokens[2].strip()
					else:
						self.deviceData[(lastVendor, devicecode)] = tokens[2].strip()
						raise customExceptions.PciIdsMultipleEntries("Multiple instances of device with the same id and vendor detected")

		except IOError:
			raise customExceptions.PciIdsFileNotFound("pci.ids file could not be located in directory")


	def getVendorName(self,venhex):
		vencode = util.stripvalue(venhex, True)	
		try:
			result = self.vendorData[vencode]
			return result
		except KeyError:
			raise customExceptions.PciIdsFailedSearch("Could not find vendor: %s" % venhex)

	def getDeviceName(self,venhex, devhex):
		vencode = util.stripvalue(venhex, True)
		devcode = util.stripvalue(devhex, True)
		try:
			result = self.deviceData[(vencode, devcode)]
			return result
		except KeyError:
			raise customExceptions.PciIdsFailedSearch("Could not find device: %s of vendor: %s" % (devhex, venhex))



def parseLine_Sep(line, key, separatorList=""):
	"""Reads single line, gets value from key-value pair delimited by separator
	   Separators are read in order of listing, first one which gives a valid value is chosen"""

	value = "NO_VALUE"
	separatorList = util.toList(separatorList)
	
	#obtains whatever is on the right of the separator, without whitespaces on the left		
	try:
	
		keyEndPos = line.index(key)	
	except ValueError:
		raise customExceptions.KeyNotFound("Key %s not found in data" % (key))	
	
	valueStringWithSeparator = line[keyEndPos+len(key):]

	

	for separator in separatorList:
		separatorExists = valueStringWithSeparator.find(separator)
	
		if separatorExists is not -1: #can find the specified separator
			valueStringNoSeparator = valueStringWithSeparator[valueStringWithSeparator.find(separator) + 1:]
			value = valueStringNoSeparator.lstrip()
			break

	if value is "":
		value = "NO_VALUE"

	
	return value
	
	

def parseData_Sep(data, key, separatorList=""):
		"Searches entire block of extracted data, gets value from key-value pair delimited by separator"		
		found = False
		value = "NO_VALUE"
		for line in data.splitlines():		
						
			try: 
				value = parseLine_Sep(line, key, separatorList)	
								
			except customExceptions.KeyNotFound: #key not found in line				
				pass
		
			else:
				#Found key!
				found = True
				break
			
		if found is False:
			raise customExceptions.KeyNotFound("Key %s not found in data" % (key))			
			
		return value


def findLine(data, key):
	"Searches data for key, and returns line which contains key"
	found = False	
	for line in data.splitlines():
		if key in line:
			found = True
			return line
	if found is False:
		raise customExceptions.KeyNotFound("Key %s not found in data" % key)
		return ""
	

def count(data, key):
	"Counts number of occurrences of key in extracted data"
	return data.count(key)





