import pytest
import glob

from UtkBase.biosFile import BiosFile
from UtkBase.utility import diffBinary


TEST_BIOS_FILE_PATHS = glob.glob("./images/*")


@pytest.mark.parametrize('filename', TEST_BIOS_FILE_PATHS)
def test_bios(filename):
    try:
        fileHandle = open(filename, 'rb')
    except Exception as ex:
        print("Could not open File at: {}".format(filename))
        assert False

    BINARY = fileHandle.read()
    fileHandle.close()

    BiosFile.disableExceptionHandling()
    bios = BiosFile.fromBinary(BINARY)
    serializedBios = bios.serialize()

    assert len(BINARY) == len(serializedBios), "Length missmatch: {} where it should be {}".format(hex(len(BINARY)), hex(len(serializedBios)))
    BINARIES_EQUAL = diffBinary(BINARY, serializedBios)
    assert BINARIES_EQUAL, "Must equal"
