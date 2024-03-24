import struct
from typing import Any

from UtkBase.uefiGuid import UefiGuid
from interfaces import Header


class ExternalVolumeHeader(Header):
    @staticmethod
    def _struct() -> struct:
        return struct.Struct('<16s I I')

    @classmethod
    def fromBinary(cls, binary: bytes) -> 'ExternalVolumeHeader':
        """

        :param binary:
        :return:
        """
        HEADER_BINARY = binary[:cls._struct().size]
        GUID_BINARY, headerSize, unknown = cls._struct().unpack(HEADER_BINARY)
        uefiGuid = UefiGuid.fromBinary(GUID_BINARY)
        header = cls(uefiGuid, headerSize, unknown)
        return header

    def __init__(self, uefiGuid: UefiGuid, headerSize, unknown):
        self._volumeGuid: UefiGuid = uefiGuid
        self._headerSize = headerSize                           # NOTE The uefiTool parser expects and asserts if this isn't 0x14
        self._unknown = unknown

    def getVolumeGuid(self) -> UefiGuid:
        return self._volumeGuid

    def getSize(self) -> int:
        return self._struct().size

    def toDict(self) -> dict[str, Any]:
        return {
            "class": self.__class__.__name__,
            "guid": self._volumeGuid,
            "headerSize": self._headerSize,
            "unknown": self._unknown
        }

    def toString(self) -> str:
        outString = "{:<20} {:<10} {:<10}\n".format("Ex. HeaderGuid", "Ex. HeaderSize", "Unknown")
        outString += "{:<20} {:<10} {:<10}\n".format(self._volumeGuid.toString(), hex(self._headerSize), hex(self._unknown))
        return outString

    def serialize(self) -> bytes:
        return self._struct().pack(self._volumeGuid.serialize(), self._headerSize, self._unknown)
