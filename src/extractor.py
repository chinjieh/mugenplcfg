#Module that handles extraction of data
import customExceptions

def extractData(loc):	
	"Simply reads the entire file from loc and returns it"
	##If fails, IOError exception is thrown
	trimmedDataString = "";
	with open(loc) as fileToBeRead:
	
		#obtain the data to be read - with a \n at the back	
		dataString = fileToBeRead.read();
	
		#remove trailing newline
		trimmedDataString = dataString.rstrip();

	return trimmedDataString; 


import struct
def extractBinaryData(file, start, bytes, endian="BIG_ENDIAN"):
	"Reads binary file at start position and returns bytes read as list of bytes in hex"
	with open(file, "rb") as f:
		BYTE_SIZE = 1
		bytelist = []
		f.seek(start)
		byte = f.read(BYTE_SIZE)
		
		while bytes is not 0:
			if byte != "":
				intbyte = struct.unpack('B', byte)[0]
				hexbyte = "{:02x}".format(intbyte)
				if endian is "BIG_ENDIAN":
					bytelist.append(hexbyte)
				elif endian is "LITTLE_ENDIAN":
					bytelist.insert(0, hexbyte)
				else:
					raise ValueError("Incorrect argument value '%s' for argument 'endian' in function: extractBinaryData" % endian)
				bytes -= 1
				byte = f.read(BYTE_SIZE)
			else:
				raise customExceptions.NoAccessToFile("No permission to read file: %s" % file)
	return bytelist



def extractBinaryLinkedList(file, startpos, datasize, nextoffset=1, stopid=0x00, numJumps=-1):
	"Extracts binary data that is in linked list format i.e reads address from startpos, reads data in address, reads address from ptroffset..."
	result = []	
	
	def readdata(f,size):
		data = f.read(size)
		if data != "":
			#returns integer of data
			return struct.unpack('B', data)[0]
		else:
			raise customExceptions.NoAccessToFile("No permission to read file: %s" % file)

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



"""
import io
import binascii
def printBinaryData(loc):
	"Used to print data from a binary file like 'config' in pci devices"
	with open(loc, "rb") as f:
		chunksize = 1
		byte = f.read(chunksize)
		asciiarray = []
		while byte != b"":
			bytestring = binascii.b2a_hex(byte)
			asciiarray.append(bytestring)
			byte = f.read(chunksize)
		
		for i in range(0, len(asciiarray)):
				print asciiarray[i]			
			
		#for i in range (0,len(asciiarray), 2):
		#	print hex(i), ": ", asciiarray[i+1], asciiarray[i]
		#	print " "
"""
		
