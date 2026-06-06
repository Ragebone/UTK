import os
import shutil

import pytest
import glob

from UtkBase.biosFile import BiosFile

from tools.extract import export


def only_directories(list_of_path: list[str]) -> list[str]:
    output = []
    for path in list_of_path:
        if os.path.isdir(path):
            continue

        output.append(path)

    return output


TEST_BIOS_FILE_PATHS = only_directories(glob.glob("images/*"))


@pytest.mark.parametrize('filename', TEST_BIOS_FILE_PATHS)
def test_extract_import(filename):
    try:
        fileHandle = open(filename, 'rb')
    except Exception as ex:
        print("Could not open File at: {}".format(filename))
        assert False

    BINARY = fileHandle.read()
    fileHandle.close()

    outputDirectory = os.path.join("/tmp", filename + ".d")

    if os.path.exists(outputDirectory):
        print("Deleting {} first\n".format(outputDirectory))
        shutil.rmtree(outputDirectory)

    os.makedirs(outputDirectory)
    print("Extracting {} to: {}\n".format(filename, outputDirectory))

    bios = BiosFile.fromBinary(BINARY)

    export(bios, outputDirectory, 0xff)
