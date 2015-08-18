#Module to contain custom exceptions
class CustomException(Exception):
	def __init__(self,msg=""):
		self.msg = msg
		super(CustomException, self).__init__(msg)
		
class MSRFileNotFound(CustomException):
	pass

class CapabilityUnknown(CustomException):
	pass

class DeviceCapabilitiesNotRead(CustomException):
	pass

class InvalidAttribute(CustomException):
	pass

class AttributeMismatch(CustomException):
	pass

class PyxbgenInvalidSchema(CustomException):
	pass

class NoAccessToFile(CustomException):
	pass

class ProcessorSpeedNotFound(CustomException):
	pass

class PciIdsFileNotFound(CustomException):
	pass

class PciIdsFailedSearch(CustomException):
	pass

class PciIdsMultipleEntries(CustomException):
	pass

class PciIdsSubclassNotFound(CustomException):
	pass

class PciIdsInvalidLink(CustomException):
	pass

class DmarFileNotFound(CustomException):
	pass

class DmarFileNotCopied(CustomException):
	pass

class IaslToolNotFound(CustomException):
	pass

class KeyNotFound(CustomException):
	pass

class ForceQuit(CustomException):
	pass

class InsufficientPermissions(CustomException):
	pass
