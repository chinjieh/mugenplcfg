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
from src import message, customExceptions, update, bindings, output


def init():
    # Initialise PyXB binding file
    bindings.init(paths.SCHEMAPATH, paths.SCHEMA_BINDING_PATH)


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
        try:
            checkPermissions()
        except customExceptions.InsufficientPermissions:
            print ("mugenplcfg must be run with root permissions. "
                   "Try running with 'sudo'.")
        else:
            main(args.force)


def main(forcecreate=False):
    print "=== Mugenplcfg Start ==="

    print "> Initialising..."
    init()
    from src import creator, schemadata

    try:
        print "> Extracting data from system..."
        elemtree = creator.createElements()
        xml = output.genXML(elemtree, 'utf-8')

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
                output.output(xml, paths.OUTPUT)
            else:
                print "> XML File could not be generated."
        else:
            output.output(xml, paths.OUTPUT)


if __name__ == "__main__":
    handleArgs()
