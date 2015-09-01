Mugenplcfg
==========


Overview
--------

`mugenplcfg` is a tool developed to support the [Muen Project][1].
It retrieves hardware information from a running Linux system and produces a
Muen platform configuration file in XML format.


Requirements
------------

`mugenplcfg` requires `iasl` (part of the acpica-tools package) to be installed.
You can get it by from its website or through Ubuntu's Advanced Packaging Tool:

    $ sudo apt-get install iasl

Optionally, `mugenplcfg` also uses the Python Package [lxml][5] to format the
generated XML file. You can get it (if not yet installed) with either:

    $ sudo apt-get install python-lxml

or

    $ sudo pip install lxml

Installing mugenplcfg
---------------------

`mugenplcfg` can be obtained from the repository with the command:

    $ git clone --recursive http://git.codelabs.ch/git/muen/mugenplcfg.git

This clones all submodules required by the tool as well as the source files.


Running mugenplcfg
------------------

After installation, `mugenplcfg` can be run with the following commands:

    $ sudo modprobe msr
    $ sudo python mugenplcfg/mugenplcfg.py

Root user permissions are necessary to allow `mugenplcfg` to examine system
data.


Output
------

After running the tool, the output XML file will be produced in the tool
directory and will be named **output.xml**.

Any errors encountered by the tool will (by default) prevent the output file
from being generated. The tool can attempt to generate an output file anyway
(for manual editing) using the `-f / --force` argument.


Updating
--------

As the tool relies on external files (such as the [pci.ids][3] repository), some
of these files might need to be updated to retrieve accurate information.
You can utilise the `-u / --update` argument to download and update these files
automatically. 


Optional Arguments
------------------

- `-u / --update`             Update files used by the tool
- `-f / --force`              Attempt to generate the output file despite errors
- `-g SCHEMA /--gen SCHEMA`   Generates a .py binding file from a .xsd schema


More about mugenplcfg
---------------------

### How it works

`mugenplcfg` scans Linux system files (*/sys, /proc, /dev*) for processor,
memory and device information needed by the Muen kernel. It then fills up
**PyXB** Python objects with the information and creates an XML file.


### Use of PyXB Library

`mugenplcfg` utilises the [PyXB package][2] to generate
a Python binding file from a platform configuration schema file. This binding
file is then used to create and fill objects that are later converted to XML in
the output. This pre-generated file is located at 
*/schemaconfig/schemaconfig.py* in the tool directory.

The **PyXB** package is included as a submodule in the `mugenplcfg` repository
at: */contrib/pyxb*


### Use of pci.ids

To decode device names, `mugenplcfg` parses the **pci.ids** file in
*/data/pci.ids*. **pci.ids** is a repository of PCI identification numbers 
maintained by the good people [here][3].


Running Tests
-------------

The test application for `mugenplcfg` requires the Python Package
[mock][4]. Install it with either:

    $ sudo apt-get install python-mock

or

    $ sudo pip install mock

After installing the required dependencies, the tests can be run with:

    $ python mugenplcfg/test/testApp.py


Additional information on generated platform file
-------------------------------------------------

`mugenplcfg` alters the following in the XML output platform file to match the 
requirements of the Muen Kernel:

##### Memory
  - Omit memory blocks that are reserved
  - Size of memoryBlocks are rounded down to the nearest multiple of a page
  - Sets "allocatable" to false for memoryBlocks at addresses < 1 MiB

##### Devices (PCI)
  - Omit PCI Bridges
  - Omit non PCI-Express devices behind bridges
  - Size of memoryBlocks are rounded up to match the size of a page (4KiB)

##### Devices (Serial)
  - Omits serial devices on ports other than COM ports


Contact
-------

You can drop an email to the Muen development team's mailing list at

	muen-dev@googlegroups.com

or contact the author (Chen Chin Jieh) directly at

	cchen@hsr.ch


Acknowledgements
----------------

Big thanks to Adrian and Reto for their unending guidance and advice!


[1]: http://muen.sk/ "Muen website"
[2]: http://pyxb.sourceforge.net/ "PyXB"
[3]: https://pci-ids.ucw.cz/ "The pci.ids repository"
[4]: https://mock.readthedocs.org/en/latest/ "Mock"
[5]: http://lxml.de/ "LXML" 
