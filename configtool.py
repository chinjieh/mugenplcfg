import paths
import warningmod
import os
import customExceptions

#
#	ConfigTool is developed to support the Muen Project. It produces a system policy file to be used by the Muen kernel.
#
#	ConfigTool utilises a binding configuration file generated using the library PyXB, as a representation of the XSD schema. This file is to be named 'schemaconfig.py'.
#	It also utilises pci.ids, a repository of PCI identification numbers obtained from https://pci-ids.ucw.cz/
#
##= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = 

def init():
	#Check for Pyxb binding configuration file
	try:
		open (paths.SCHEMACONFIG + ".py", "r")
	except IOError:
		raise customExceptions.SchemaConfigFileNotFound()

def runTests():
	pass

def generateXML(elemtree):
	return elemtree.toXML("utf-8")

def output(xml):
	OUTPUT_NAME = "output.xml"
	print "> Generating XML file: '%s' to location: %s" % (OUTPUT_NAME, paths.OUTPUT)
	
	xml = xml.replace('><','>\n<')
		
	with open(os.path.join(paths.OUTPUT, OUTPUT_NAME), "w") as f:
		indents = 0
		for line in xml.splitlines(True):		
			f.write(line)

def main():
	print "=== ConfigTool Start ==="

	try:
		print "> Initializing..."		
		init()

		print "> Running tests..."
		runTests()

		print "> Extracting data from schema bindings..."
		import creator
		elemtree = creator.createElements()
		xml = generateXML(elemtree)

		output(xml)
		warningmod.printWarnings()

		if len(warningmod.warnings) is 0:
			print "=== ConfigTool completed successfully ==="
		else:
			print "=== ConfigTool completed with %d warning(s) ===" % len(warningmod.warnings)

	except customExceptions.SchemaConfigFileNotFound:
		print "Could not find required PyXB binding file '%s.py' in tool directory.\nPlease ensure that the file is there and try again." % paths.SCHEMACONFIG
	
if __name__ == "__main__":
	main()

