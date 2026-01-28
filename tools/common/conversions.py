import enum

from UtkAmd.utkAmdInterfaces import UtkAMD
from utkInterfaces import Serializable, Reference


class BINARY(enum.Enum):
    NO = 0
    SOME = 1
    ALL = 2


def recursiveToDict(dictionary: dict[str, any]) -> dict:
    """

    :param dictionary:
    :return:
    """
    newDict = {}

    for key, item in dictionary.items():

        if isinstance(item, Serializable):
            newDict[key] = recursiveToDict(item.toDict())
            continue

        if isinstance(item, int):
            newDict[key] = hex(item)
            continue

        if isinstance(item, bytes):
            binary: bytes = item
            newDict[key] = binary.hex().upper()
            continue

        if isinstance(item, enum.Enum):
            item: enum.Enum = item
            newDict[key] = {
                "name": item.name,
                "value": item.value
            }

        if isinstance(item, Reference):
            newDict[key] = convertItem(item, depth=1)
    return newDict


def convertItem(item: any, depth: int = 0, includeBinary: BINARY = BINARY.ALL) -> any:
    if isinstance(item, (Serializable)):
        if depth <= 0:
            return {
                "class": item.__class__.__name__,
            }

        return convertDict({
            item.__class__.__name__: item.toDict()
        }, depth - 1)

    if isinstance(item, dict):
        return convertDict(item, depth - 1)

    if isinstance(item, list):
        valueList: list = item
        newList = []
        for listItem in valueList:
            newItem = convertItem(listItem, depth - 1)
            newList.append(newItem)

        return newList

    if isinstance(item, int):
        return hex(item)

    if isinstance(item, bytes):
        match includeBinary:
            case BINARY.NO:
                return "Binary",
            case BINARY.SOME:
                return item[:256].hex().upper()
            case BINARY.ALL:
                return item.hex().upper()

    if isinstance(item, enum.Enum):
        return {
            "name": item.name,
            "value": item.value
        }

    if isinstance(item, Reference):

        if not isinstance(item, UtkAMD):
            return {
                "reference": "TODO"
            }

        return {
            "offset": hex(item.getOffset())
        }
    return item


def convertDict(dictionary: dict[str, any], depth: int = 0) -> dict[str, any]:
    outputDict = {}
    for key, value in dictionary.items():
        outputDict[key] = convertItem(value, depth - 1)
    return outputDict
