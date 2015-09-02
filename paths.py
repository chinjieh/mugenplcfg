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

# File containing paths
# =====================
import os
CURRENTDIR = os.path.dirname(__file__)

## Location of tmp folder
TEMP = CURRENTDIR + "/tmp/"

## Location of system files / directories
CPUINFO = "/proc/cpuinfo"
MEMMAP = "/sys/firmware/memmap/"
DEVICES = "/sys/bus/pci/devices/"
IOMEM = "/proc/iomem"
MSR = ["/dev/cpu/0/msr", "/dev/msr0"]
IOPORTS = "/proc/ioports"
DMAR = "/sys/firmware/acpi/tables/DMAR"
DMAR_TEMP = TEMP
DEVMEM = "/dev/mem"

## Location of pci.ids
PCIIDS = CURRENTDIR + "/data/pci.ids"

## Location of PyXB Library
PYXB = CURRENTDIR + "/contrib/pyxb/"
PYXB_GEN = PYXB + "scripts/pyxbgen"

## Location of schemaconfig : PyXB binding file
SCHEMACONFIGPATH = CURRENTDIR +"/schemaconfig/"
SCHEMACONFIG = CURRENTDIR + "/schemaconfig/schemaconfig"

## Location of output file
OUTPUT = CURRENTDIR + "/"

