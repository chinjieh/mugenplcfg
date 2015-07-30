#Module to contain custom exceptions
class CustomException(Exception):
	def __init__(self,msg=""):
		self.msg = msg
		super(CustomException, self).__init__(msg)

class CapabilityUnknown(CustomException):
	pass

class InvalidAttribute(CustomException):
	pass

class AttributeMismatch(CustomException):
	pass

class NoAccessToFile(CustomException):
	pass

class PciIdsFileNotFound(CustomException):
	pass

class PciIdsFailedSearch(CustomException):
	pass

class PciIdsMultipleEntries(CustomException):
	pass

class PciIdsSubclassNotFound(CustomException):
	pass

class SchemaConfigFileNotFound(CustomException):
	pass

class KeyNotFound(CustomException):
	pass
