#Module to contain utility functions
import math
import os

# == Utility Classes ==
class ListNumberer():
	"Class that stores list of names, and is able to retrieve numbered names"
	def __init__(self, listnames):
		self.listnames = listnames
		self.namecount = {} #name, count of how many times name was used
		self.NUMBER_FORMAT = "_%d"

	def getName(self, inname):
		repeatednames = []
		outname = ""

		if inname not in self.listnames:
			raise ValueError("ListNumberer.getName: 'inname' not in 'listnames'")

		for name in self.listnames:
			if name not in repeatednames:
				if self.listnames.count(name) > 1:
					repeatednames.append(name)
		
		if inname in repeatednames:
			if inname in self.namecount:
				self.namecount[inname] += 1
			else:
				self.namecount[inname] = 1
			outname = inname + self.NUMBER_FORMAT % self.namecount[inname]	
		else:
			outname = inname

		return outname

# == Misc functions ==
def toList(keylist):
	"Convert keylist to a list"
	if type(keylist) is not list:
		if type(keylist) is tuple:
			keylist = list(keylist)
		else:
			keylist = [keylist]

	return keylist

def removeListsFromList(mainList, *removelists):
	"Removes elements in removelists from mainList"
	result = []
	toremove = []
	#Fills toremove with index numbers of elements to ignore
	for item in mainList:
		if mainList.index(item) not in toremove:
			for removelist in removelists:
				if item in removelist:
					toremove.append(mainList.index(item))
	#Add elements to result while ignoring those in toremove
	for item in mainList:
		if mainList.index(item) not in toremove:	
			result.append(item)
	return result

def getBit(number, bitno):
	"Gets bit value from number"
	if number & int(math.pow(2,bitno)):
		return 1
	else:
		return 0

def getLinks(path, filterexp=None):
	"Returns list of absolute links in path (with optional filter)"
	filelist = []

	if filterexp is None:
		def filterexp(filename):
			return True

	files = sorted(os.listdir(path))

	for filename in files:
		if filterexp(filename):
			#Get the absolute location of symbolic links in path
			filePath = os.path.join(path,filename)
			relativeLink = os.readlink(filePath)
			absLink = os.path.join(os.path.dirname(filePath), relativeLink)			
			filelist.append(absLink)

	return filelist

def numberMultiples(listin):
	"Numbers repeated elements in list, leaves it alone if element is solo"
	NUMBER_FORMAT = "_%d"
	repeatednames = []
	namecount = {} #name, count
	for name in listin:
		if name not in repeatednames:
			if listin.count(name) > 1:
				repeatednames.append(name)

	listout = []
	for name in listin:
		if name in repeatednames:
			if name not in namecount:
				namecount[name] = 1
			else:
				namecount[name] += 1
			newname = name + NUMBER_FORMAT % namecount[name]
			listout.append(newname)
		else:
			listout.append(name)
			
	return listout

# == Functions to support generation of schema ==


def isHex(value):
	if isinstance(value,basestring):
		return value.startswith("0x")
	else:
		return False

def toWord64(value):
	"Converts to Word64 Type"
	rawvalue = stripvalue(value)
	#Pads string to be length of multiple of 4, justified right
	value = rawvalue.rjust(int(math.ceil( len(rawvalue)/4.0) *4 ), '0')
	#Add underscore between characters
	finalvalue = ""
	
	for index in range(0,len(value)):
		if ((index % 4) is 0) and (index is not 0):
			finalvalue += "_"

		finalvalue += value[index]	
	
	return 	wrap16(finalvalue)
	
def wrap16(value):
	"Wraps value -> 16#value#"
	wrapper = "16#_#"
	return wrapper.replace("_", value)

def spacesToUnderscores(value):
	"Converts spaces to underscores"
	return value.replace(" ", "_")

def stripvalue(value, retainzeros = False):
	"Strips a number to obtain the raw value with/without leading 0s"
	if isHex(value):
		result = value.partition('0x')[-1]
		if retainzeros is False:
			result = result.lstrip('0')
		
		if result == "":
			return "0"
		else:
			return result 
	else:
		return value
		
def sizeOf(addr1, addr2):
	"Gets size between two hex addresses"
	if isHex(addr1) and isHex(addr2):
		int1 = int(addr1,16)
		int2 = int(addr2,16)
		diff = abs(int2 - int1) + 1 #Add one for correct size (include start)
		return hex(diff)
	else:
		print "sizeOf has to accept 2 hexadecimal values"
		raise ValueError
