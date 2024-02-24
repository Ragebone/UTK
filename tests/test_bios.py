import traceback
from unittest import TestCase

from UtkBase.bios import Bios
from UtkBase.utility import diffBinary
from tests import TEST_BIOS_FILE_PATHS


class TestBios(TestCase):
    def test_end_to_end(self) -> None:
        fileHandles = []
        for filePath in TEST_BIOS_FILE_PATHS:
            try:
                fileHandle = open(filePath, 'rb')
            except Exception as ex:
                print("Could not open File at: {}".format(filePath))
                continue

            fileHandles.append(fileHandle)

        success = True
        for fileHandle in fileHandles:
            BINARY = fileHandle.read()
            FILE_NAME = fileHandle.name
            fileHandle.close()

            try:
                bios = Bios.fromBinary(BINARY)
            except Exception as ex:
                success = False
                traceback.print_exception(type(ex), ex, ex.__traceback__)
                continue

            try:
                serializedBios = bios.serialize()
            except Exception as ex:
                success = False
                traceback.print_exception(type(ex), ex, ex.__traceback__)
                continue

            print("\nDiffing: {}\n".format(FILE_NAME))
            BINARIES_EQUAL = diffBinary(BINARY, serializedBios)
            if not BINARIES_EQUAL:
                success = False

        assert success, "serialization failed"

