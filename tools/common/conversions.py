import enum
from typing import Any, List

from utkInterfaces import Serializable


def convertItem(item: Any, depth: int = 0):
    if isinstance(item, Serializable):
        if depth <= 0:
            return {
                "class": item.__class__.__name__,
            }

        return convertDict({
            item.__class__.__name__: item.toDict()
        }, depth - 1)

    if isinstance(item, dict):
        return convertDict(item, depth - 1)

    if isinstance(item, List):
        valueList: List = item
        newList = []
        for listItem in valueList:
            newItem = convertItem(listItem, depth - 1)
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


def convertDict(dictionary: dict[str, any], depth: int = 0) -> dict[str, Any]:
    outputDict = {}
    for key, value in dictionary.items():
        outputDict[key] = convertItem(value, depth - 1)
    return outputDict
