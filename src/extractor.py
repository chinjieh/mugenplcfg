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
def extractBinaryData(file, start, bytes, endian="BIG_ENDIAN", chunks=False):
	"Reads binary file at start position and returns bytes read, or as list of"
	"bytes if chunks=True"
	with open(file, "rb") as f:
		BYTE_SIZE = 1
		bytelist = []
		f.seek(start)
		byte = f.read(BYTE_SIZE)
		result = ""
		while bytes is not 0:
			if byte != "":
				intbyte = struct.unpack('B', byte)[0]
				if chunks:
					hexbyte = "0x{:02x}".format(intbyte)
					if endian is "LITTLE_ENDIAN":
						bytelist.append(hexbyte)
					elif endian is "BIG_ENDIAN":
						bytelist.insert(0, hexbyte)
					else:
						raise ValueError("Incorrect argument value '%s' " % endian +
										 "for argument 'endian' in function: "
										 "extractBinaryData")
				else:
					result = "{:02x}".format(intbyte) + result
				bytes -= 1
				byte = f.read(BYTE_SIZE)
			else:
				raise customExceptions.NoAccessToFile("No permission to read "
													  "file: %s" % file)
	if chunks:
		return bytelist
	else:
		return "0x" + result



def extractBinaryLinkedList(file, startpos, datasize, nextoffset=1, stopid=0x00, numJumps=-1):
	"Extracts binary data that is in linked list format i.e "
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