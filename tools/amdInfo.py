import argparse
import enum
import json
import logging

from UtkAmd.psp.zenReference import ZenReference
from UtkAmd.utkAmdInterfaces import UtkAMD
from UtkBase.biosFile import BiosFile
from utkInterfaces import Serializable
from tools.common.loggerSettings import applyLogSettings, addLoggingFlags


def convertItemForAMD(item: any, depth: int = 0):
    if isinstance(item, Serializable):
        if depth <= 0 and not isinstance(item, UtkAMD):
            return {
                "class": item.__class__.__name__,
            }

        return convertDict({
            item.__class__.__name__: item.toDict()
        }, depth - 1)

    if isinstance(item, dict):
        return convertDict(item, depth)

    if isinstance(item, list):
        valueList: list = item
        newList = []
        for listItem in valueList:
            newItem = convertItemForAMD(listItem, depth - 1)
            newList.append(newItem)

        return newList

    if isinstance(item, bytes):
        return "Binary"

    if isinstance(item, enum.Enum):
        return {
            "name": item.name,
            "value": item.value
        }

    if isinstance(item, ZenReference):
        return {
            "class": item.__class__.__name__,
            "absoluteOffset": item.getAbsoluteOffset()
        }

    return item


def convertDict(dictionary: dict[str, any], depth: int = 0) -> dict[str, any]:
    outputDict = {}
    for key, value in dictionary.items():
        outputDict[key] = convertItemForAMD(value, depth - 1)
    return outputDict


def main():
    argParser = argparse.ArgumentParser(
        prog="UTK AMD Info",
        description='Print specifics of all known AMD parts of the given BiosFile\nOutput-format is  JSON',
        epilog="Use -h or --help for more information"
    )
    # Application default Arguments
    addLoggingFlags(argParser)

    argParser.add_argument('filenames', metavar='F', type=str, nargs='+', help='File / Path Bios file')

    arguments = vars(argParser.parse_args())

    applyLogSettings(arguments)

    filePaths = arguments.get("filenames")
    for path in filePaths:
        # BiosFile.disableExceptionHandling()

        try:
            bios = BiosFile.fromFilepath(path)
        except Exception as ex:
            if BiosFile.dontHandleExceptions:
                raise ex
            logging.error(ex.__traceback__)
            print("Failed parsing from {}".format(path))
            continue

        print("{}\n".format(path))
        biosDict = convertItemForAMD(bios, 3)
        string = json.dumps(biosDict, indent=4)
        print(string)


if __name__ == "__main__":
    main()
