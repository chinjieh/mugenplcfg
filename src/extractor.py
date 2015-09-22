#   Copyright (C) 2015 Chen Chin Jieh <chinjieh@gmail.com>
#   Copyright (C) 2015 Reto Buerki <reet@codelabs.ch>
#   Copyright (C) 2015 Adrian-Ken Rueegsegger <ken@codelabs.ch>
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


# Module that handles extraction of data
import customExceptions


def extractData(loc):
    "Simply reads the entire file from loc and returns it"
    # If fails, IOError exception is thrown
    trimmedDataString = ""
    with open(loc) as fileToBeRead:

        # obtain the data to be read - with a \n at the back
        dataString = fileToBeRead.read()

        # remove trailing newline
        trimmedDataString = dataString.rstrip()

    return trimmedDataString

import struct


def extractBinaryData(file, start, bytes, endian="BIG_ENDIAN", chunks=False):

    """
    Reads binary file at start position and returns bytes read, or as list
    of bytes if chunks=True"""

    with open(file, "rb") as f:
        BYTE_SIZE = 1
        bytelist = []
        f.seek(start)
        byte = f.read(BYTE_SIZE)
        result = ""
        while bytes is not 0:
            if byte != "":
                intbyte = struct.unpack('B', byte)[0]
                if chunks:
                    hexbyte = "0x{:02x}".format(intbyte)
                    if endian == "LITTLE_ENDIAN":
                        bytelist.append(hexbyte)
                    elif endian == "BIG_ENDIAN":
                        bytelist.insert(0, hexbyte)
                    else:
                        raise ValueError("Incorrect argument value '%s' " %
                                         endian + "for argument 'endian' in "
                                         "function: extractBinaryData")
                else:
                    result = "{:02x}".format(intbyte) + result
                bytes -= 1
                byte = f.read(BYTE_SIZE)
            else:
                raise customExceptions.NoAccessToFile("No permission to read "
                                                      "file: %s" % file)
    if chunks:
        return bytelist
    else:
        return "0x" + result
