#File containing paths
from os import path

CURRENTDIR = path.dirname(__file__)

PATH_TEST = CURRENTDIR + "/test/"
PATH_TEST_EXTRACTOR = CURRENTDIR + "/test/extractor/"
PATH_TEST_EXTRACTOR_MEMORYCREATOR = PATH_TEST_EXTRACTOR + "memorycreator/"
PATH_TEST_PARSEUTIL = CURRENTDIR + "/test/parseutil/"
PATH_TEST_SCHEMADATA = CURRENTDIR + "/test/schemadata/"
PATH_TEST_CREATOR = CURRENTDIR + "/test/creator/"

CPUINFO = "/proc/cpuinfo"
MEMMAP = "/sys/firmware/memmap/"
DEVICES = "/sys/bus/pci/devices/"
PCIIDS = CURRENTDIR + "/data/"
IOMEM = "/proc/iomem"
SCHEMACONFIGPATH = CURRENTDIR +"/"
SCHEMACONFIG = "schemaconfig"
OUTPUT = CURRENTDIR + "/"
MSR = ["/dev/cpu/0/msr", "/dev/msr0"]
