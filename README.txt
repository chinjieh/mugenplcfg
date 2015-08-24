## README FILE ##


# mugenplcfg is a tool developed to support the Muen Project. It produces a
# system policy file to be used by the Muen kernel.
#
# mugenplcfg utilises a binding configuration file generated using the library 
# PyXB, as a representation of the XSD schema. This file is to be named 
# 'schemaconfig.py'.
#
# It also utilises pci.ids, a repository of PCI identification numbers obtained 
# from https://pci-ids.ucw.cz/
#
##= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = 


== [ Requirements ] ==

mugenplcfg requires iasl (part of the acpia-tools package) to be installed.
You can get it by from its website or through Ubuntu's Advanced Packaging Tool:
	
	$ sudo apt-get install iasl


== [ Installing mugenplcfg ] ==

mugenplcfg can be obtained from the repository with the command:

	$ git clone --recursive git@git.codelabs.ch:/muen/mugenplcfg

This clones all submodules required by the tool as well as the source files.


== [ Running mugenplcfg ] ==

After installation, mugenplcfg can be run with the command:

	$ sudo python mugenplcfg/mugenplcfg.py

Root user permissions are necessary to allow mugenplcfg to examine system data.


== [ Optional Arguments ] ==

-u / --update			Update files used by the tool
-f / --force			Attempt to generate the output file despite errors
-g SCHEMA /--gen SCHEMA		Generates a .py binding file from a .xsd schema file


== [ Running Tests ] ==

The test application for mugenplcfg requires the Python Package 'mock'
(website: https://mock.readthedocs.org/en/latest/ )
Install it with the command:

	$ sudo pip install mock

After installing the required dependencies, the tests can be run with:

	$ python mugenplcfg/test/testApp.py


== [ Additional information on generated platform file ] ==

mugenplcfg alters the following in the platform file to match the requirements
of the Muen Kernel:

Memory :
	- Omit memory blocks that are reserved
	- Size of memoryBlocks are rounded down to the nearest multiple of a page
	- Sets "allocatable" to false for memoryBlocks at address < 1 MiB

Devices (PCI):
	- Omit PCI Bridges
	- Omit non PCI-Express devices behind bridges
	- Size of memoryBlocks are rounded up to match the size of a page (4KiB)

Devices (Serial):
	- Omits serial devices on ports other than COM ports
