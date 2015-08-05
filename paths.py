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
TTY = "/proc/ioports"
DMAR = "/sys/firmware/acpi/tables/DMAR"
DMAR_TEMP = TEMP
DEVMEM = "/dev/mem"

## Location of pci.ids
PCIIDS = CURRENTDIR + "/data/pci.ids"

## Location of schemaconfig : PyXB binding file
SCHEMACONFIGPATH = CURRENTDIR +"/schemaconfig/"
SCHEMACONFIG = CURRENTDIR + "/schemaconfig/schemaconfig"

## Location of output file
OUTPUT = CURRENTDIR + "/"

