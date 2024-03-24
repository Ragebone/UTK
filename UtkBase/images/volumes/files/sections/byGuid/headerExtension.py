import struct
from typing import Any

from UtkBase.uefiGuid import UefiGuid
from interfaces import Header


class HeaderExtension(Header):
    @classmethod
    def _struct(cls):
        return struct.Struct('<16s H H')

    @classmethod
    def fromBinary(cls, binary: bytes) -> 'HeaderExtension':
        guidBinary, dataOffset, attributes = cls._struct().unpack(binary[:cls._struct().size])
        guid = UefiGuid.fromBinary(guidBinary)
        guidString = guid.toString()

        return cls(guid, dataOffset, attributes)

    def __init__(self, guid: UefiGuid, dataOffset: int, attributes: int):
        self._guid: UefiGuid = guid
        self._dataOffset = dataOffset
        self._attributes = attributes

    def getSize(self) -> int:
        return self._struct().size

    def getGuidString(self) -> str:
        return self._guid.toString()

    def toDict(self) -> dict[str, Any]:
        return {
            "class": self.__class__.__name__,
            "guid": self._guid,
            "dataOffset": self._dataOffset,
            "attributes": self._attributes
        }

    def toString(self) -> str:
        return "HeaderExtension"

    def serialize(self) -> bytes:
        return self._struct().pack(self._guid.serialize(), self._dataOffset, self._attributes)
