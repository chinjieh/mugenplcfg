import sys; sys.dont_write_bytecode = True
import paths
import os
from src import customExceptions, creator, message

#
# ConfigTool is developed to support the Muen Project. It produces a system
# policy file to be used by the Muen kernel.
#
# ConfigTool utilises a binding configuration file generated using the library 
# PyXB, as a representation of the XSD schema. This file is to be named 
# 'schemaconfig.py'.
#
# It also utilises pci.ids, a repository of PCI identification numbers obtained 
# from https://pci-ids.ucw.cz/
#
##= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = 

def init():
	#Check for Pyxb binding configuration file
	try:
		open (paths.SCHEMACONFIG + ".py", "r")
	except IOError:
		message.addError("Could not find required PyXB binding file 'schemaconfig.py' " +
			"in location: %s.\nPlease ensure that the file is there " + 
			"and try again." % (paths.SCHEMACONFIG))

def checkPermissions():
	"Check user permissions"
	if not os.access("/sys", os.W_OK):
		message.addMessage("ConfigTool cannot be run without the proper " + \
			"permissions. Try running with 'sudo'.", True)

def formatXML(xmlstr):
	"Uses lxml to format xml string"
	print "Formatting XML document..."
	result = xmlstr
	try:
		from lxml import etree
	except ImportError:
		message.addWarning("Lxml library not found, could not format XML document")
	else:
		root = etree.fromstring(xmlstr)
		result = etree.tostring(root, pretty_print=True)

	return result	
	
def generateXML(elemtree):
	xmlstr = elemtree.toXML("utf-8")
	formattedxml = formatXML(xmlstr)
	return formattedxml

def output(xml):
	OUTPUT_NAME = "output.xml"
	print "> XML file '%s' generated to location: \n %s" % (OUTPUT_NAME, 
								paths.OUTPUT )

	#xml = xml.replace('><','>\n<')
	with open(os.path.join(paths.OUTPUT, OUTPUT_NAME), "w") as f:
		indents = 0
		for line in xml.splitlines(True):
			f.write(line)

def hasErrors():
	hasErrors = False
	for key in message.messagecount:
		if key is message.ErrorMessage:
			hasErrors = True

	return hasErrors


def main():
	print "=== ConfigTool Start ==="

	checkPermissions()
	print "> Initializing..."
	init()

	print "> Extracting data from schema bindings..."
	elemtree = creator.createElements()
	xml = generateXML(elemtree)

	message.printMessages()

	if len(message.messagequeue) is 0:
		print "=== ConfigTool completed successfully ==="
	else:
		print "ConfigTool finished with: "
		for key in message.messagecount:
			print "%d %s" % (message.messagecount[key],
					key.shortname)

	if hasErrors():
		print "> XML File could not be generated."
	else:
		output(xml)
	
if __name__ == "__main__":
	main()

