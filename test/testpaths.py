#File containing paths for tests
import os
CURRENTDIR = os.path.dirname(__file__)

PATH_TEST_EXTRACTOR = CURRENTDIR + "/extractor/"
PATH_TEST_EXTRACTOR_MEMORYCREATOR = PATH_TEST_EXTRACTOR + "memorycreator/"
PATH_TEST_PARSEUTIL = CURRENTDIR + "/parseutil/"
PATH_TEST_SCHEMADATA = CURRENTDIR + "/schemadata/"
PATH_TEST_CREATOR = CURRENTDIR + "/creator/"
PATH_TEST_UTIL = CURRENTDIR + "/util/"
PATH_TEST_UPDATE = CURRENTDIR + "/update/"
PATH_TEST_DEVICECAP = CURRENTDIR + "/devicecap/"
PATH_TEST_BINDINGS = CURRENTDIR + "/bindings/"

PATH_PCIIDS = os.path.join(CURRENTDIR, "testpciids")
PATH_IOPORTS = os.path.join(PATH_TEST_CREATOR, "devicescreator/test_ioports")
PATH_DEVICELINKS = os.path.join(PATH_TEST_CREATOR,"devicescreator/devices_test_links")
PATH_SCHEMA = os.path.join(CURRENTDIR, "testschema.xsd")

PATH_TEST_GEN = CURRENTDIR + "/gen/"
