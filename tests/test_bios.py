import pytest
import glob

from UtkBase.biosFile import BiosFile

from UtkBase.utility import diffBinary


TEST_BIOS_FILE_PATHS = glob.glob("images/*")


@pytest.mark.parametrize('filename', TEST_BIOS_FILE_PATHS)
def test_biosFile(filename):
    try:
        fileHandle = open(filename, 'rb')
    except Exception as ex:
        print("Could not open File at: {}".format(filename))
        assert False

    BINARY = fileHandle.read()
    fileHandle.close()

    BiosFile.disableExceptionHandling()
    bios = BiosFile.fromBinary(BINARY)

    images = bios.getImages()
    for image in images:
        imageOffset = image.getOffset()
        imageContent = image.getContent()

        for offset, imageElement in imageContent:
            elementBinary = imageElement.serialize()
            ABSOLUTE_ELEMENT_OFFSET = imageElement.getOffset() + imageOffset
            actualBinary = BINARY[ABSOLUTE_ELEMENT_OFFSET:ABSOLUTE_ELEMENT_OFFSET + len(elementBinary)]
            assert len(actualBinary) == len(elementBinary), "Length missmatch: {} where it should be {}".format(hex(len(elementBinary)), hex(len(actualBinary)))
            assert diffBinary(actualBinary, elementBinary), "Must equal"

