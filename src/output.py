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


# Module to handle generation of output file
import os
import paths
import message
import subprocess
import parseutil
import util
import customExceptions
import importlib

SPACES_MAIN = 5
SPACES_SUB = 7
    
def produce_toolver():
    "Produces tool version using git describe"
    success = True
    result = produceLine("Generated with mugenplcfg.", SPACES_MAIN)
    try:
        version = _runCommand("git describe --always",
                              "Tool version in output description could not "
                              "be obtained.")
    except customExceptions.FailedOutputCommand:
        success = False
    else:
        result = produceLine("Generated with mugenplcfg (commit %s)" % version,
                             SPACES_MAIN)

    return result, success

def _runCommand(commandstr, errmsg):
    result = None
    command = commandstr.split()
    try:
        subprocess.check_call(command,
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE)
    except (subprocess.CalledProcessError, OSError) as e:
        warning = (errmsg + " Subprocess '%s' encountered an error > %s" %
                   (commandstr, e) )
        message.addWarning(warning)
        raise customExceptions.FailedOutputCommand(str(e))
    else:
        proc = subprocess.Popen(command,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        result = proc.communicate()[0].strip()
    
    return result

    
def produce_linuxver():
    "Produces linux version using uname"
    success = True
    result = produceLine("Linux kernel version: ", SPACES_MAIN)
    try:
        version = _runCommand("uname -r", "Linux kernel version in output "
                              "description could not be obtained.")
    except customExceptions.FailedOutputCommand:
        success = False
    else:
        result = produceLine("Linux kernel version: %s" % version, SPACES_MAIN)

    return result, success

def produce_distver():
    "Produces distribution version using lsb_release"
    success = True
    DESCRIPTION_KEY = "Description"
    result = produceLine("Distribution: ", SPACES_MAIN)
    try:
        distdata = _runCommand("lsb_release -a",
                               "Dist version in output description could not "
                               "be obtained.")
    except customExceptions.FailedOutputCommand:
        success = False
    else:
        distdesc = parseutil.parseData_Sep(distdata, DESCRIPTION_KEY, ":")
        result = produceLine("Distribution: %s" % distdesc, SPACES_MAIN)

    return result, success

def produce_biosinfo():
    "Produces bios information"
    success = True
    result = produceLine("BIOS information:",SPACES_MAIN)
    try:
        dmiparser = parseutil.DMIParser(paths.DMI)
        result += produceLine("Vendor: %s" % dmiparser.getData("bios_vendor"),
                              SPACES_SUB)
        result += produceLine("Version: %s" %
                              dmiparser.getData("bios_version"),
                              SPACES_SUB)
        result += produceLine("Date: %s" % dmiparser.getData("bios_date"),
                              SPACES_SUB)
    except Exception as e:
        message.addWarning("BIOS information in output description could not "
                           "be obtained: %s" % e)
        success = False
    return result, success

def produce_productinfo():
    "Produces product information"
    success = True
    result = produceLine("Product information:", SPACES_MAIN)
    try:
        dmiparser = parseutil.DMIParser(paths.DMI)
        result += produceLine("Vendor: %s" %
                              dmiparser.getData("product_vendor"),
                              SPACES_SUB)
        result += produceLine("Name: %s" %
                              dmiparser.getData("product_name"),
                              SPACES_SUB)
        result += produceLine("Product Version: %s" %
                              dmiparser.getData("product_version"),
                              SPACES_SUB)
        result += produceLine("Chassis Version: %s" %
                              dmiparser.getData("chassis_version"),
                              SPACES_SUB)
        result += produceLine("Serial: %s" %
                              dmiparser.getData("product_serial"),
                              SPACES_SUB)

    except Exception as e:
        message.addWarning("Product information in output description could "
                           "not be obtained: %s" % e)
        success = False
    return result, success

def produceHeader(*producers):
    "Produces descriptive header comment code"
    BORDER_WIDTH = 42
    topborder = "<!-- " + ("=" * BORDER_WIDTH) + "\n"
    header = topborder
    for producer in producers:
        header += producer()[0]
    header += "     " + ("=" * BORDER_WIDTH) + " -->\n"

    return header

def produceLine(info, lspace):
    "Produces a line in the header"
    line = ""
    if info != "":
        line += " " * lspace
        line += info
        line += "\n"
    
    return line

def formatXML(xmlstr, encoding):
    "Uses lxml to format xml string"
    print "Formatting XML document..."
    result = xmlstr
    success = True
    try:
        formatmodule = importmodule("lxml.etree")
    except ImportError:
        message.addWarning(
            "LXML library not found, could not format XML document.")
        success = False
    else:
        root = formatmodule.fromstring(xmlstr)
        result = formatmodule.tostring(root, pretty_print=True,
                                       xml_declaration=True,
                                       encoding=encoding)
    return result, success

def importmodule(modulestr):
    "Import a module"
    etree = importlib.import_module(modulestr)
    return etree


def genXML(elemtree, encoding):
    "Produce entire xml string from elemtree"
    xmlstr = elemtree.toXML(encoding)
    xml = formatXML(xmlstr, encoding)[0]
    
    # Find declaration
    xmltokens = xml.partition("?>")
    xml_declare = xmltokens[0] + xmltokens[1]
    xml_body = xmltokens[2]
    
    # Produce header
    header = produceHeader(
        produce_toolver,
        produce_linuxver,
        produce_distver,
        produce_biosinfo,
        produce_productinfo
    )
    
    # Combine declaration with header and body
    xml = xml_declare + "\n" + header + "\n" + xml_body

    return xml

def output(xml, outpath):
    OUTPUT_NAME = os.path.basename(outpath)

    print "> XML file '%s' generated to location: \n %s" % (
        OUTPUT_NAME, outpath)

    with open(outpath, "w") as f:
        for line in xml.splitlines(True):
            f.write(line)