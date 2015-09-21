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


# Module to contain custom exceptions
class CustomException(Exception):

    def __init__(self, msg=""):
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


class FailedOutputCommand(CustomException):
    pass
