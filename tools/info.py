import argparse
import logging
import traceback
from typing import List, BinaryIO

from UtkBase.bios import Bios
from tools.common.loggerSettings import applyLogSettings, addLoggingFlags


def main():
    argParser = argparse.ArgumentParser(
        prog="UTK Info",
        description='Print all known information contained within a BiosFile',
        epilog="Use -h or --help for more information"
    )
    # Application default Arguments
    addLoggingFlags(argParser)

    argParser.add_argument('filenames', metavar='F', type=str, nargs='+', help='File / Path Bios file')
    arguments = vars(argParser.parse_args())

    applyLogSettings(arguments)

    filePaths = arguments.get("filenames")
    fileHandles: List[BinaryIO] = []
    for path in filePaths:
        try:
            fileHandle = open(path, 'rb')
            fileHandles.append(fileHandle)
        except:
            error = "Could not open File at: {}".format(path)
            logging.error(error)
            print(error)
            continue

    for fileHandle in fileHandles:
        BINARY = fileHandle.read()
        FILE_NAME = fileHandle.name
        fileHandle.close()

        try:
            bios = Bios.fromBinary(BINARY)
        except Exception as ex:
            traceback.print_exception(type(ex), ex, ex.__traceback__)
            error = "Failed parsing from {}".format(fileHandle.name)
            logging.error(error)
            print(error)
            continue

        print("{}\n".format(FILE_NAME))
        print(bios.toString())


if __name__ == "__main__":
    main()
