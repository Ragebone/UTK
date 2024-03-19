import struct
from typing import Any

from UtkBase.uefiGuid import UefiGuid


class ToshibaCapsuleHeader:
    """
    A Toshiba capsule header implementation
    TODO add reference to the UEFITool or other references
    """
    @classmethod
    def _struct(cls) -> struct:
        return struct.Struct('<16sIII')     # CapsuleGuid HeaderSize FullSize flags

    @classmethod
    def fromBinary(cls, binary: bytes) -> 'ToshibaCapsuleHeader':
        GUID_BINARY, headerSize, capsuleSize, flags = cls._struct().unpack(binary[:cls._struct().size])
        guid = UefiGuid.fromBinary(GUID_BINARY)

        return cls(guid, headerSize, capsuleSize, flags)

    def __init__(self, guid: UefiGuid, headerSize: int, fullSize: int, flags: int):
        assert guid.toString() in [
            "539182B9-ABB5-4391-B69A-E3A943F72FCC"
        ], f"Wrong guid for ToshibaCapsuleHeader, got {guid.toString()}"

        self._capsuleGuid = guid
        self._capsuleSize = headerSize
        self._fullSize = fullSize
        self._flags = flags

    def getSize(self) -> int:
        return self._struct().size

    def getCapsuleSize(self) -> int:
        # TODO verify that the "header size" matches with the RomImageOffset, otherwise, this is a problem
        return self._capsuleSize

    def getEncapsulatedImageSize(self) -> int:
        return self._fullSize

    def toDict(self) -> dict[str, Any]:
        return {
            "class": self.__class__.__name__,
            "guid": self._capsuleGuid,
            "capsuleSize": self._capsuleSize,
            "flags": self._flags,
            "capsuleImageSize": self._fullSize
        }

    def serialize(self):
        binary = self._struct().pack(self._capsuleGuid.serialize(), self._capsuleSize, self._fullSize, self._flags)
        return binary
