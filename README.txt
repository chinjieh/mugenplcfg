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




== [ Running the Tool ] ==

ConfigTool requires root user permissions to execute correctly.
It can be run via the command:

$ sudo python ./configtool.py

== [ Optional Arguments ] ==

-u / -update		Update files used by the tool


