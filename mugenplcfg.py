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
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   << About mugenplcfg >>
#
#   mugenplcfg is a tool developed to support the Muen Project (http://muen.sk).
#   It retrieves hardware information from a running Linux system and produces a
#   Muen platform configuration file in XML format.
#
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =


import sys
sys.dont_write_bytecode = True
import argparse
import paths
import os
import shutil
from src import customExceptions, message, update

def cleanup():
    "Call this function at the end of the program to remove temp files"
    print "Cleaning up..."
    CURRENTDIR = os.path.dirname(__file__)
    shutil.rmtree(paths.TEMP, onerror=cleanupErrorHandler)


def cleanupErrorHandler(function, path, excinfo):
    message.addWarning("Could not remove temp directory: %s" % path)


def checkPermissions():
    "Check user permissions"
    if not os.access("/sys", os.W_OK):
        raise customExceptions.InsufficientPermissions()


def formatXML(xmlstr):
    "Uses lxml to format xml string"
    print "Formatting XML document..."
    result = xmlstr
    try:
        from lxml import etree
    except ImportError:
        message.addWarning(
            "LXML library not found, could not format XML document.")
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

    print "> XML file '%s' generated to location: \n %s" % (
        OUTPUT_NAME, os.path.join(paths.OUTPUT, OUTPUT_NAME))

    with open(os.path.join(paths.OUTPUT, OUTPUT_NAME), "w") as f:
        for line in xml.splitlines(True):
            f.write(line)


def hasErrors():
    hasErrors = False
    for key in message.messagecount:
        if key is message.ErrorMessage:
            hasErrors = True
    return hasErrors


def handleArgs():
    "Checks arguments in command line and performs relevant actions"
    descriptiontext = (
        "mugenplcfg is a tool which extracts system information and produces "
        "an .xml file to be used in the Muen kernel.")
    parser = argparse.ArgumentParser(description=descriptiontext)

    parser.add_argument("-u", "--update",
                        help="Updates files used by the tool",
                        action="store_true")
    parser.add_argument("-f", "--force",
                        help="Attempts to generate the output file despite "
                        "errors",
                        action="store_true")
    args = parser.parse_args()

    runMain = True
    if args.update:
        update.update()
        runMain = False

    if runMain:
        main(args.force)


def main(forcecreate=False):
    print "=== Mugenplcfg Start ==="

    try:
        checkPermissions()
        from src import creator, schemadata

        print "> Extracting data from schema bindings..."
        elemtree = creator.createElements()
        xml = generateXML(elemtree)

    except customExceptions.InsufficientPermissions:
        print ("mugenplcfg must be run with root permissions. "
               "Try running with 'sudo'.")

    except customExceptions.ForceQuit:
        message.printMessages()
        cleanup()
        print "> XML File could not be generated."
        sys.exit()

    else:   
        message.printMessages()
        cleanup()
        if len(message.messagequeue) is 0:
            print "=== Mugenplcfg completed successfully ==="
        else:
            print "mugenplcfg finished with: "
            for key in message.messagecount:
                print "%d %s" % (message.messagecount[key],
                                 key.shortname)
            print "========================================="

        if hasErrors():
            if forcecreate:
                output(xml)
            else:
                print "> XML File could not be generated."
        else:
            output(xml)


if __name__ == "__main__":
    handleArgs()
