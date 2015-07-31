#Module to contain utility functions
import math

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
