#   Copyright (C) 2015 Chen Chin Jieh <cchen@hsr.ch>
#
#   This file is part of mugenplcfg.
#
#   mugenplcfg is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   mugenplcfg is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with mugenplcfg.  If not, see <http://www.gnu.org/licenses/>.


# Module to update tool
import paths
import urllib
import urllib2
import shutil
import customExceptions
import parseutil
import extractor
import schemadata
import os

PCI_IDS = "https://pci-ids.ucw.cz/v2.2/pci.ids"


def update():
    success = True
    print "Updating tool..."
    if not updatePciIds(PCI_IDS, paths.PCIIDS):
        success = False
        
    if not updateSchemaBinding(paths.SCHEMAPATH, paths.SCHEMA_BINDING_PATH):
        success = False
        
    if success:
        print "Update completed."
    else:
        print "Update completed with errors."

    return success


def updatePciIds(url, location):
    success = True
    localfile = False
    print "> Attempting to update file: %s" % location
    try:
        print "Checking for resource file @ '%s'" % url
        urllib2.urlopen(url)
    except (urllib2.URLError):
        print "Failed to update file: %s" % location
        print "> pci.ids file could not be updated from url: %s" % url
        print "> The file can be obtained manually from the repository."
        success = False
        raise customExceptions.PciIdsInvalidLink()
    except ValueError:
        # Might not be url, might be local file
        localfile = True

    print "Updating file: %s" % location
    oldver = ""
    newver = ""
    with open(location) as oldfile:
        for line in oldfile.readlines():
            if "Version:" in line:
                oldver = parseutil.parseLine_Sep(line, "Version", ":").strip()
                break

    if not localfile:
        urllib.urlretrieve(url, location)
    else:
        shutil.copy(url, location)

    with open(location) as newfile:
        for line in newfile.readlines():
            if "Version" in line:
                newver = parseutil.parseLine_Sep(line, "Version", ":").strip()
                break
    print "pci.ids updated: Version %s > %s" % (oldver, newver)
    return success
    
def updateSchemaBinding(schemapath, bindingpath):
    "Re-generates the PyXB binding file from the schema"
    success = False
    print "> Attempting to update schema bindings..."
    BINDING_FOLDER = os.path.dirname(bindingpath)
    BINDING_NAME = os.path.splitext(os.path.basename(bindingpath))[0]
    try:
        schemadata.createBindings(schemapath,
                                  BINDING_FOLDER,
                                  BINDING_NAME,
                                  paths.PYXB_GEN)
    except Exception as e:
        print "Schema binding updating failed: %s" + str(e)
        
    else:
        print "Schema bindings updated successfully."
        success = True

    return success
