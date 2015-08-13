## README FILE ##


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


== [ Installing the Tool ] ==

ConfigTool can be obtained from the repository via command:

	$ git clone --recursive git@git.codelabs.ch:/muen/mugenplcfg

This clones all submodules required by the tool as well as the source files.


== [ Running the Tool ] ==

After installation, ConfigTool can be run via the command:

	$ sudo python mugenplcfg/configtool.py

Root user permissions are necessary to allow ConfigTool to examine system data.


== [ Optional Arguments ] ==

-u / --update				Update files used by the tool
-f / --force				Attempt to generate the output file despite errors
-g SCHEMA /--gen SCHEMA		Generates a .py binding file from a .xsd schema file


== [ Additional information on generated platform file ] ==

mugenplcfg alters the following in the platform file to match the requirements
of the Muen Kernel:

Memory :
	- Omit memory blocks that are reserved
	- Size of memoryBlocks are rounded down to the nearest multiple of a page
	- Sets "allocatable" to false for memoryBlocks with a size < allocatable (1MB)

Devices (PCI):
	- Omit PCI Bridges
	- Omit non PCI-Express devices behind bridges
	- Size of memoryBlocks are rounded up to match the size of a page

Devices (Serial):
	- Omits serial devices on ports other than COM ports
