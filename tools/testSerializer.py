import argparse

from UtkBase.biosFile import BiosFile
from UtkBase.utility import diffBinary
from tools.common.loggerSettings import applyLogSettings, addLoggingFlags


def main():
    argParser = argparse.ArgumentParser(
        prog="test-serializer",
        description='Basically like the pytest, just for a single file to ease debugging',
        epilog="Use -h or --help for more information"
    )
    # Application default Arguments
    addLoggingFlags(argParser)

    argParser.add_argument('filenames', metavar='F', type=str, nargs='+', help='File / Path Bios file')
    arguments = vars(argParser.parse_args())

    applyLogSettings(arguments)

    filePaths = arguments.get("filenames")
    for path in filePaths:

        fileHandle = open(path, 'rb')
        BINARY = fileHandle.read()
        fileHandle.close()

        BiosFile.disableExceptionHandling()

        bios = BiosFile.fromFilepath(path)

        images = bios.getImages()
        for image in images:
            imageOffset = image.getOffset()
            imageContent = image.getContent()

            for offset, imageElement in imageContent:
                elementBinary = imageElement.serialize()
                ABSOLUTE_ELEMENT_OFFSET = imageElement.getOffset() + imageOffset
                actualBinary = BINARY[ABSOLUTE_ELEMENT_OFFSET:ABSOLUTE_ELEMENT_OFFSET + len(elementBinary)]
                assert len(actualBinary) == len(elementBinary), "Length missmatch: {} where it should be {}".format(
                    hex(len(elementBinary)), hex(len(actualBinary)))
                assert diffBinary(actualBinary, elementBinary), "Must equal"


if __name__ == "__main__":
    main()
