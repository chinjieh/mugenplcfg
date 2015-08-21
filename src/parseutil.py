#Module containing utilities for parsing data
import util
import extractor
import os
import shutil
import subprocess
import message
import customExceptions

class PciIdsParser():
	"Class used to parse pci.ids file"
	VENDOR_LENGTH = 4
	DEVICE_LENGTH = 4
	CLASS_LENGTH = 2
	SUBCLASS_LENGTH = 2
	def __init__(self, pciIdsLoc):
		#initialise personal dictionary to decode vendor and device codes
		self.vendorData = {} #vencode = venname
		self.deviceData = {} #(vencode, devcode) = devname
		self.classData = {} #classcode = classname
		self.init(pciIdsLoc)

	def isValidVendorCode(self,code):
		result = True
		if len(code) is not PciIdsParser.VENDOR_LENGTH:
			result = False
		if code.isalnum() is False:
			result = False
		return result

	def isValidDeviceCode(self,code):
		result = True
		if len(code) is not PciIdsParser.DEVICE_LENGTH:
			result = False
		if code.isalnum() is False:
			result = False
		return result

	def isValidClassCode(self,code):
		result = True
		if len(code) is not PciIdsParser.CLASS_LENGTH:
			result = False
		if code.isalnum() is False:
			result = False
		return result

	def isValidSubclassCode(self,code):
		result = True
		if len(code) is not PciIdsParser.SUBCLASS_LENGTH:
			result = False
		if code.isalnum() is False:
			result = False
		return result

	def isVendor(self,line):
		if self.isValidVendorCode(line.partition("  ")[0]):
			return True
		else:
			return False

	def isDevice(self,line):
		result = False
		if self.isVendor(line) is False:
			if line.startswith("\t") :
				if line.count("\t") is 1:
					if self.isValidDeviceCode(line.partition("  ")[0].lstrip()):
						result = True
		return result

	def isClass(self,line):
		result = False
		if line.startswith("C"):
			if self.isValidClassCode(line.split(" ")[1]):
				result = True
		return result

	def isSubclass(self,line):
		result = False
		if line.startswith("\t"):
			if not line.startswith("\t\t"):
				if self.isValidSubclassCode(line.lstrip().partition("  ")[0]):
					result = True
		return result

	def init(self,pciIdsLoc):
		"Fills up database from pci.ids at pciIdsLoc"
		try:
			data = extractor.extractData(pciIdsLoc)
			lastVendor = ""
			lastClass = ""
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
						raise customExceptions.PciIdsMultipleEntries(
							"Multiple instances of vendor with the same id detected")

				#if find Device, refer to last Vendor
				if self.isDevice(line):
					tokens = line.lstrip("\t").partition("  ")
					devicecode = tokens[0].strip()
					if (lastVendor, devicecode) not in self.deviceData:
						self.deviceData[(lastVendor, devicecode)] = tokens[2].strip()
					# Will not fail as isVendor will detect the duplicate first,
					# leaving this here in case
					#else:
						#self.deviceData[(lastVendor, devicecode)] = tokens[2].strip()
						#raise customExceptions.PciIdsMultipleEntries(
						#	"Multiple instances of device with the same id and "
						#	"vendor detected")

				#find Class
				if self.isClass(line):
					lastClass = line.split(" ")[1] #gets class code
					self.classData["%s" % lastClass] = line.split("  ")[1] #gets class name

				#if find Subclass, refer to last Class
				if self.isSubclass(line):
					tokens = line.lstrip().partition("  ")
					subclassname = tokens[2]
					self.classData["%s%s" % (lastClass,tokens[0])] = subclassname

		except IOError:
			raise customExceptions.PciIdsFileNotFound("pci.ids file could not be "
													 "located in directory")

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
			raise customExceptions.PciIdsFailedSearch(
				"Could not find device: %s of vendor: %s" % (devhex, venhex) )

	def getClassName(self,clshex):
		"Searches first 4 digits of class code e.g. 0604 in self.classData"
		clscode = util.stripvalue(clshex, True)
		result = ""
		try:
			result = self.classData[clscode]

		except KeyError: #Could not find subclass, trying to find class...
			try:
				result = self.classData[clscode[:PciIdsParser.CLASS_LENGTH]]
				raise customExceptions.PciIdsSubclassNotFound(
					"Could not find subclass: %s" % clshex)

			except KeyError:
				raise customExceptions.PciIdsFailedSearch(
					"Could not find class: %s" % clshex)

		return result


class DMARParser():
	"Handles parsing of DMAR table"
	
	def __init__(self):
		self.copiedDMAR = None
		self.parsedDMAR = None
	
	def genDMAR(self, dmar, outputloc):
		"Copies DMAR file to temp folder, call this first"
		success = False

		outputfolder = os.path.dirname(outputloc)
		#Make temp folder
		self._genDMAR_maketempfolder(outputfolder)
		
		#Copy DMAR file to temp folder
		if self._genDMAR_copyDMAR(dmar, outputloc):
			success = True
			self.copiedDMAR = outputloc
		return success
			
	def _genDMAR_maketempfolder(self, loc):
		"""Makes a temp folder if does not exist"""
		if not os.path.isdir(loc):
			os.makedirs(loc)
			
	def _genDMAR_copyDMAR(self, src, dest):
		success = True
		#Check if DMAR exists
		try:
			open(src,"r")
		except IOError:
			#DMARFileNotFound
			message.addMessage("No DMAR file found at: '%s'; " % src +\
							   "No IOMMU devices found.")
			success = False
		else:
			#Copy DMAR to temp folder
			try:
				shutil.copyfile(src, dest)
			except IOError:
				message.addMessage("DMAR table at: '%s' " % src +\
								 "could not be copied to location: '%s'" % dest)
				#DmarFileNotCopied
				message.addError("Could not obtain DMAR information; IOMMU device "
								   "information not found.", False)
				success = False
				
		if success:
			self.copiedDMAR = dest
				
		return success
	
	def getParsedDmarPath(self):
		return self.parsedDMAR
	
	def getCopiedDmarPath(self):
		return self.copiedDMAR
	
	def parseDMAR(self, dmarfilepath=None):
		"Parses dmarfile with iasl"
		success = True
		if dmarfilepath is None:
			dmarfilepath = self.getCopiedDmarPath()
		dmarfilepath_noext, ext = os.path.splitext(dmarfilepath)
		outfile = dmarfilepath_noext + ".dsl"
		try:
			self._runIasl(dmarfilepath)
		except OSError:
				#IaslToolNotFound
				message.addMessage("iasl tool not found in the system. "+
						"Try 'apt-get install iasl' to install.")
				message.addError("Could not obtain DMAR information; IOMMU device "
								"information not found.", False)
				success = False
		else:
			self.parsedDMAR = outfile
				
		return success
	
	def _runIasl(self,dmarfilepath):
		subprocess.check_call(["iasl", "-d", dmarfilepath])
	
	"""
	def parseDMAR(self, iaslcmdstr):
		"Evaluates iaslcmdstr as a function to parse DMAR information."
		success = True
		try:
			exec(iaslcmdstr)
		except OSError as e:
			if e.errno == os.errno.ENOENT:
				#IaslToolNotFound
				message.addMessage("iasl tool not found in the system. "+
						"Try 'apt-get install iasl' to install.")
				message.addError("Could not obtain DMAR information; IOMMU device "
								"information not found.", False)
				success = False
			else:
				raise
				
		return success
	"""

	def getIommuAddrs(self, parsedDMAR=None):
		"Retrieves Register Base Addresses of IOMMUs from parsed DMAR"
		iommuaddrs = []
		KEY = "Register Base Address"
		if parsedDMAR is None:
			parsedDMAR = self.getParsedDmarPath()
		try:
			dmardata = extractor.extractData(parsedDMAR)
		except IOError:
			message.addError("Could not find parsed DMAR file in location: %s." %
							 parsedDMAR, False)
		else:
			for line in dmardata.splitlines():
				try:
					addr = parseLine_Sep(line, KEY, ":")
					addr = addr.lstrip("0")
					addr = "0x" + addr
					addr = addr.lower()
					iommuaddrs.append(addr)

				except customExceptions.KeyNotFound:
					pass

		return iommuaddrs


def parseLine_Sep(line, key, separatorList=""):
	"""Reads single line, gets value from key-value pair delimited by separator
	   Separators are read in order of listing, first one which gives a valid
	   value is chosen"""

	value = "NO_VALUE"
	separatorList = util.toList(separatorList)

	#obtains whatever is on right of the separator, without whitespaces on left
	try:
		keyEndPos = line.index(key)
	except ValueError:
		raise customExceptions.KeyNotFound("Key %s not found in data" % (key))

	valueStringWithSeparator = line[keyEndPos+len(key):]

	for separator in separatorList:
		separatorExists = valueStringWithSeparator.find(separator)

		if separatorExists is not -1: #can find the specified separator
			valueStringNoSeparator = valueStringWithSeparator[
				valueStringWithSeparator.find(separator) + 1:]
			value = valueStringNoSeparator.lstrip()
			break

	if value is "":
		value = "NO_VALUE"

	return value

def parseData_Sep(data, key, separatorList=""):
		"Searches entire block of extracted data, gets value from key-value pair"
		"delimited by separator"
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

def findLines(data, key):
	"Searches data for key, and returns lines which contain key"
	result = []
	found = False
	for line in data.splitlines():
		if key in line:
			found = True
			result.append(line)
	if found is False:
		raise customExceptions.KeyNotFound("Key %s not found in data" % key)

	return result


def count(data, key):
	"Counts number of occurrences of key in extracted data"
	return data.count(key)





