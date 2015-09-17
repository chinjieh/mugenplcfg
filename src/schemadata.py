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


# Module to contain code related to construction of XML document
import sys
import os
import pwd
import copy
import util
import shutil
import customExceptions
import paths
import subprocess
sys.path.append(paths.PYXB)
import pyxb
sys.path.append(os.path.dirname(paths.SCHEMA_BINDING_PATH))
import platformconfig as schema


class Element():

    "Class that wraps Pyxb and provides easier use of modification of XML elements"

    # How to use this class:
    # 1. Create the element using the constructor, with the relevant fields
    #    for "name" and "elemtype" corresponding to schema
    #
    #	 e.g. processor = Element("processor", "processorType")
    #
    # 2. Set attributes by using []. Multiple attributes can be set at once too.
    #
    #	 e.g. processor["attribute1"] = value1    OR
    #         processor["attribute1", "attribute2"] = value1, value2
    #
    # 3. Set element content by using setContent("elementContent")
    #
    # 4. Add child elements to the element by using appendChild(Element)
    #
    #	 e.g. processorChild = Element("processorChild", "processorChildType")
    #	      processor.appendChild(processorChild)
    #
    # 5. When the whole element tree has been created, call toXML('utf version')
    #    on the root element. This will convert the entire tree to XML format.
    #	 e.g. xml = processor.toXML('utf-8')

    def __init__(self, name, elemtype):
        "name: schema's name attribute; elemtype: schema's 'type' "
        self.name = name
        self.type = elemtype
        self.childElements = []
        self.parent = None
        self.content = ""
        self.attr = {}  # holds attributes of Element

    def compileToPyxb(self):
        "Converts the Element class to a Pyxb Binding Type"
        if self.content:
            pyxbElem = getattr(schema, self.type)(self.content)
        else:
            pyxbElem = getattr(schema, self.type)()
        # Fill up attributes of Pyxb binding element
        for key in self.attr:
            setattr(pyxbElem, key, self.attr[key])

        # Adds children elements to Pyxb binding element
        if self.childElements:
            self.__addChildElements(pyxbElem)

        return pyxbElem

    def toXML(self, utf):
        "Returns XML representation of the element"
        elempyxb = self.compileToPyxb()
        xml = elempyxb.toxml(utf, element_name=self.name)
        return xml

    def __setitem__(self, keylist, valuelist):
        pyxbElem = getattr(schema, self.type)

        keylist = util.toList(keylist)
        valuelist = util.toList(valuelist)
        if valuelist == [""]:
            pass
        else:
            if len(keylist) != len(valuelist):
                errorstr = (("Values %s to be assigned to attributes %s in element %s "
                             "do not match in length") % (valuelist, keylist, self))
                raise customExceptions.AttributeMismatch(errorstr)
            else:
                for index in range(0, len(keylist)):
                    key = keylist[index]
                    if key not in dir(pyxbElem):
                        raise customExceptions.InvalidAttribute(
                            "Element %s does not have attribute: %s" % (self, key))
                    else:
                        self.attr[key] = valuelist[index]

    def __getitem__(self, key):
        pyxbElem = getattr(schema, self.type)
        if key not in dir(pyxbElem):
            raise customExceptions.InvalidAttribute(
                "Element %s does not have attribute: %s" % (self, key))
        else:
            return self.attr[key]

    def __addChildElements(self, pyxbElem):
        "Adds elements in childElements to pyxbElem"

        pluralNameList = []

        for element in self.childElements:
            if element.name not in pluralNameList:
                try:
                    setattr(pyxbElem, element.name, element.compileToPyxb())

                # if element to be added is required to be in a list
                except pyxb.SimplePluralValueError:
                    self.__setPluralElems(
                        pyxbElem, self.__getSimilarElems(element.name))
                    # Append pluralNameList so as to not check similar elements
                    # of same name
                    pluralNameList.append(element.name)

    def __getSimilarElems(self, elemName):
        "Creates list of elements with names matching elemName in childElement list"
        elemList = [
            element for element in self.childElements if (element.name == elemName)]
        return elemList

    def __setPluralElems(self, pyxbElem, pluralElems):
        "Set attribute of Pyxb object to list of plural elements"
        pluralPyxb = []
        for e in pluralElems:
            pluralPyxb.append(e.compileToPyxb())

        setattr(pyxbElem, pluralElems[0].name, pluralPyxb)

    def getParent(self):
        return self.parent

    def setContent(self, data):
        self.content = data

    def appendChild(self, *elems):
        "Add elements in 'elems' as child of this element"
        success = True
        if type(elems[0]) is list:
            elems = tuple(elems[0])
        for elem in elems:
            if elem is None:
                success = False
            else:
                elem.parent = self
                self.childElements.append(elem)

        return success

    def removeChild(self, obj):
        "Removes single Element object from child of this element"
        if obj in self.childElements:
            obj.parent = None
            self.childElements.remove(obj)

    def isEqual(self, elem2):
        """
        Compares all attributes and contents of this element including children.
        Children have to be added in the similar order for it to equate. """
        if self.attr != elem2.attr or self.content != elem2.content:
            return False
        else:
            if len(self.childElements) != len(elem2.childElements):
                return False
            else:
                for counter in range(len(self.childElements)):
                    if not self.childElements[counter].isEqual(elem2.childElements[counter]):
                        return False

        return True
