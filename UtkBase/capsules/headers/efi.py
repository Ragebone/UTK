import struct

from UtkBase.capsules.headers.headerInterface import CapsuleHeader


class EfiCapsuleHeader(CapsuleHeader):

    @classmethod
    def _struct(cls):
        return struct.Struct('<16sIII')     # CapsuleGuid HeaderSize Flags CapsuleImageSize

    @classmethod
    def fromBinary(cls, binary: bytes):
        return cls(*cls._struct().unpack(binary[:cls._struct().size]))

    def __init__(self, capsuleGuid, headerSize, flags, capsuleImageSize):
        # TODO use UefiGuid
        self._capsuleGuid = capsuleGuid
        self._headerSize = headerSize
        self._flags = flags
        self._capsuleImageSize = capsuleImageSize

    def getSize(self):
        # TODO switch to the struct size?
        return self._headerSize

    def getCapsuleSize(self) -> int:
        # TODO verify correctness
        return self._headerSize

    def getEncapsulatedImageSize(self) -> int:
        return self._capsuleImageSize

    def toDict(self) -> dict[str, any]:
        return {
            "class": self.__class__.__name__,
            "guid": self._capsuleGuid,
            "capsuleSize": self._headerSize,
            "flags": self._flags,
            "capsuleImageSize": self._capsuleImageSize
        }

    def serialize(self):
        binary = self._struct().pack(self._capsuleGuid, self._headerSize, self._flags, self._capsuleImageSize)
        return binary
