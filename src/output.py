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
    
def produce_toolver():
    "Produces tool version using git describe"
    result = "Generated with mugenplcfg"
    commandstr = "git describe --always"
    command = commandstr.split()
    try:
        subprocess.check_output(command, stderr=subprocess.STDOUT)
    except Exception as e:
        message.addWarning("Tool version in output description could not be "
                           "obtained: Subprocess '%s' encountered an error > %s"
                           % (commandstr, e.output))
    else:
        proc = subprocess.Popen(command, stdout=subprocess.PIPE)
        version = proc.communicate()[0].strip()
        result = "Generated with mugenplcfg (commit %s)" % version

    return result
    
def produce_linuxver():
    "Produces linux version using uname"
    result = "Linux kernel version: "
    commandstr = "uname -r"
    command = commandstr.split()
    try:
        subprocess.check_call(command, stdout=subprocess.PIPE)
    except OSError as e:
        message.addWarning("Linux kernel version in output description could "
                           "not be obtained: Subprocess '%s' encountered an "
                           "error > %s"% (commandstr, e))
    else:
        proc = subprocess.Popen(command, stdout=subprocess.PIPE)
        version = proc.communicate()[0].strip()
        result = "Linux kernel version: %s" % version

    return result

def produce_distver():
    "Produces distribution version using lsb_release"
    DESCRIPTION = "Description"
    result = "Distribution: "
    commandstr = "lsb_release -a"
    command = commandstr.split()
    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT)
    except OSError as e:
        message.addWarning("Dist version in output description could not be "
                           "obtained: Subprocess '%s' encountered an error > %s"
                           % (commandstr, e))
    else:
        proc = subprocess.Popen(command,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        distdata = proc.communicate()[0]
        distdesc = parseutil.parseData_Sep(distdata, DESCRIPTION, ":")
        result = "Distribution: %s" % distdesc

    return result

def produceHeader():
    "Produces descriptive header comment code"
    LINE_WIDTH = 50
    BORDER_WIDTH = LINE_WIDTH - 5
    producers = [
        produce_toolver,
        produce_linuxver,
        produce_distver
    ]
    border = "<!-- "
    border += "=" * BORDER_WIDTH
    border += " -->\n"
    header = border
    for producer in producers:
        line = ""
        info = producer()
        if info != "":
            line += "<!-- " + info
            line = line.ljust(LINE_WIDTH, " ")
            line += " -->"
            line += "\n"
            header += line
    header += border

    return header

def formatXML(xmlstr, encoding):
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
        result = etree.tostring(root, pretty_print=True,
                                xml_declaration=True,
                                encoding=encoding)

    return result

def genXML(elemtree, encoding):
    "Produce entire xml string from elemtree"
    xmlstr = elemtree.toXML(encoding)
    xml = formatXML(xmlstr,encoding)
    
    # Find declaration
    xmltokens = xml.partition("?>")
    xml_declare = xmltokens[0] + xmltokens[1]
    xml_body = xmltokens[2]
    
    # Combine declaration with header and body
    xml = xml_declare + "\n" + produceHeader() + "\n" + xml_body

    return xml

def output(xml):
    OUTPUT_NAME = "output.xml"

    print "> XML file '%s' generated to location: \n %s" % (
        OUTPUT_NAME, os.path.join(paths.OUTPUT, OUTPUT_NAME))

    with open(os.path.join(paths.OUTPUT, OUTPUT_NAME), "w") as f:
        for line in xml.splitlines(True):
            f.write(line)