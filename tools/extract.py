import argparse
import json
import logging
import os
import shutil

from UtkBase.biosFile import BiosFile
from tools.common.conversions import recursiveToDict
from utkInterfaces import Serializable, Header
from tools.common.loggerSettings import applyLogSettings, addLoggingFlags


def main():
    """

    :return:
    """
    argParser = argparse.ArgumentParser(
        prog="UTK Extract",
        description='Extract everything from the given BiosFile into the output directory',
        epilog="Use -h or --help for more information"
    )
    # Application default Arguments
    addLoggingFlags(argParser)
    argParser.add_argument('filenames', metavar='F', type=str, nargs='+', help='File / Path Bios file followed by the output directory')
    arguments = vars(argParser.parse_args())
    applyLogSettings(arguments)

    filePaths = arguments.get("filenames")

    assert len(filePaths) > 0, "No BiosFile was provided to be exported"
    path = filePaths[0]

    try:
        bios = BiosFile.fromFilepath(path)
    except Exception as ex:
        if BiosFile.dontHandleExceptions:
            raise ex
        logging.error(ex.__traceback__)
        print("\n\nFailed building BiosFile from:\n{}\nPossible reason:\n{}".format(path, ex))
        return 0
        # TODO it is not a good idea to always exit 0 because how are others supposed to handle different errors?
        # Not at all i guess

    outputDirectory = path + ".d"
    if len(filePaths) > 1:
        outputDirectory = filePaths[1]

    if os.path.exists(outputDirectory):
        print("Deleting {} first\n".format(path, outputDirectory))
        shutil.rmtree(outputDirectory)

    print("Extracting {} to: {}\n".format(path, outputDirectory))
    export(bios, outputDirectory)


def export(element: any, elementPath: str) -> None:
    """

    :param element:
    :param elementPath:
    :return:
    """

    # handle direct file exports first
    if isinstance(element, bytes):
        valuePath = elementPath + ".bin"
        exportToBinaryFile(valuePath, element)
        return

    if isinstance(element, Header):
        exportHeader(element, elementPath)
        return

    # left are things to go into subdirectories
    if not os.path.exists(elementPath):
        os.mkdir(elementPath)

    if isinstance(element, Serializable):
        dictionary = element.toDict()
        export(dictionary, elementPath)
        return

    if isinstance(element, list):
        for index, item in enumerate(element):
            export(item, os.path.join(elementPath, f"{index}_{item.__class__.__name__}"))
        return

    if isinstance(element, dict):
        for key, value in element.items():

            # ignore "offset" and other int values
            if isinstance(value, int):
                continue

            export(value, os.path.join(elementPath, key))
        return
    return


def exportHeader(header: Header, outputDirectory: str) -> None:
    """

    :param header:
    :param outputDirectory:
    :return:
    """
    if not os.path.exists(outputDirectory):
        os.mkdir(outputDirectory)

    headerDict = header.toDict()
    headerDict = recursiveToDict(headerDict)
    headerJson = json.dumps(headerDict, indent=4)
    headerFilePath = os.path.join(outputDirectory, header.__class__.__name__ + ".json")
    exportToJsonFile(headerFilePath, headerJson)


def exportToBinaryFile(filePath: str, binary: bytes) -> None:
    """

    :param filePath:
    :param binary:
    :return:
    """
    fileHandle = open(filePath, "wb")
    fileHandle.write(binary)
    fileHandle.close()


def exportToJsonFile(filePath: str, jsonString: str) -> None:
    """

    :param filePath:
    :param jsonString:
    :return:
    """
    fileHandle = open(filePath, "w")
    fileHandle.write(jsonString)
    fileHandle.close()


if __name__ == "__main__":
    main()
