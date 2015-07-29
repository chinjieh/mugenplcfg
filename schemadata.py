#Module to contain code related to construction of XML document
import pyxb
import copy
import util
import customExceptions
import paths
schema = __import__(paths.SCHEMACONFIG)


class Element():
	"Class that wraps Pyxb and provides easier use of modification of XML elements"

	# How to use this class:
	# 1. Create the element using the constructor, with the relevant fields for "name" and "elemtype" corresponding to schema
	#	e.g. processor = Element("processor", "processorType")
	#
	# 2. Set attributes by using []. Multiple attributes can be set at once too.
	#	e.g. processor["attribute1"] = value1    OR     processor["attribute1", "attribute2"] = value1, value2
	# 
	# 3. Set element content by using setContent("elementContent")
	#
	# 4. Add child elements to the element by using appendChild(Element)
	#	e.g. processorChild = Element("processorChild", "processorChildType")
	#	     processor.appendChild(processorChildElement)
	#
	# 5. When the whole element tree has been created, call toXML('utf version') on the root element. This will convert the entire tree to XML format.
	#	e.g. xml = processor.toXML('utf-8')

	#TODO Reject if element name is not in the schema during compileToPyxb, as Pyxb now allows any element to be created but removes them during generation of XML

	def __init__(self, name, elemtype):
		"name: schema's name attribute; elemtype: schema's 'type' "
		self.name = name
		self.type = elemtype
		self.childElements = []
		self.parent = None
		self.content = ""
		self.attr = {} #holds attributes of Element

	def compileToPyxb(self):
		"Converts the Element class to a Pyxb Binding Type"
		if self.content:
			pyxbElem = getattr(schema, self.type)(self.content)
		else:
			pyxbElem = getattr(schema,self.type)()
		#Fill up attributes of Pyxb binding element		
		for key in self.attr:
			setattr(pyxbElem,key,self.attr[key])
			
		
		#Adds children elements to Pyxb binding element
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

		if len(keylist) != len(valuelist):
			errorstr = "Values %s to be assigned to attributes %s in element %s do not match in length" % (valuelist,keylist,self)
			raise customExceptions.AttributeMismatch(errorstr)
		else:
			for index in range(0,len(keylist)):
				key = keylist[index]
				if key not in dir(pyxbElem):
					raise customExceptions.InvalidAttribute( "Element %s does not have attribute: %s" % (self, key))
				else:
					self.attr[key] = valuelist[index]

	def __getitem__(self, key):
		pyxbElem = getattr(schema, self.type)
		if key not in dir(pyxbElem):
			raise customExceptions.InvalidAttribute( "Element %s does not have attribute: %s" % (self, key) )
		else:
			return self.attr[key]
	
	def __addChildElements(self, pyxbElem):
		"Adds elements in childElements to pyxbElem"	
		
		pluralNameList = []
		
		for element in self.childElements:		
			if element.name not in pluralNameList:		
				try:
					setattr(pyxbElem, element.name, element.compileToPyxb())
					
				#if element to be added is required to be in a list
				except pyxb.SimplePluralValueError:
					self.__setPluralElems(pyxbElem, self.__getSimilarElems(element.name))
					#Append pluralNameList so as to not check similar elements of same name
					pluralNameList.append(element.name)
						

	def __getSimilarElems(self, elemName):
		"Creates list of elements with names matching elemName in childElement list"
		elemList = [element for element in self.childElements if (element.name == elemName)]
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
		for elem in elems:
			elem.parent = self
			self.childElements.append(elem)		

	def removeChild(self,obj):
		"Removes single Element object from child of this element"
		if obj in self.childElements:		
			obj.parent = None
			self.childElements.remove(obj)
	
