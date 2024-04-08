import argparse
import enum
import json
from typing import Any, List


from UtkBase.biosFile import BiosFile
from utkInterfaces import Serializable
from tools.common.loggerSettings import applyLogSettings, addLoggingFlags


def convertItem(item: Any):
    if isinstance(item, Serializable):
        return convertDict({
            item.__class__.__name__: item.toDict()
        })

    if isinstance(item, dict):
        return convertDict(item)

    if isinstance(item, List):
        valueList: List = item
        newList = []
        for listItem in valueList:
            newItem = convertItem(listItem)
            newList.append(newItem)

        return newList

    if isinstance(item, bytes):
        return "Binary"

    if isinstance(item, enum.Enum):
        return {
            "name": item.name,
            "value": item.value
        }

    return item


def convertDict(dictionary: dict[str, any]) -> dict[str, Any]:
    for key in dictionary:
        value = dictionary[key]
        dictionary[key] = convertItem(value)
    return dictionary


def main():
    argParser = argparse.ArgumentParser(
        prog="UTK Info",
        description='Print everything known about the given BiosFile(s)',
        epilog="Use -h or --help for more information"
    )
    # Application default Arguments
    addLoggingFlags(argParser)

    argParser.add_argument('filenames', metavar='F', type=str, nargs='+', help='File / Path Bios file')
    argParser.add_argument("-j", "--json", required=False, action='store_true', help="Sets the output format to json")
    argParser.add_argument("-t", "--text", required=False, action='store_true', help="Sets the output format to json")

    arguments = vars(argParser.parse_args())

    applyLogSettings(arguments)

    filePaths = arguments.get("filenames")
    for path in filePaths:
        bios = BiosFile.fromFilepath(path)
        # try:
        #     bios = BiosFile.fromFilepath(path)
        # except Exception as ex:
        #     traceback.print_exception(type(ex), ex, ex.__traceback__)
        #     error = "Failed parsing from {}".format(path)
        #     logging.error(error)
        #     print(error)
        #     continue

        print("{}\n".format(path))
        biosDict = convertItem(bios)
        string = json.dumps(biosDict, indent=4)
        print(string)


if __name__ == "__main__":
    main()
