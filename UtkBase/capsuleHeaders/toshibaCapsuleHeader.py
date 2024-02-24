import struct


class ToshibaCapsuleHeader:
    @classmethod
    def _struct(cls):
        return struct.Struct('<16sIII')     # CapsuleGuid HeaderSize FullSize flags

    @classmethod
    def fromBinary(cls, binary: bytes):
        return cls(*cls._struct().unpack(binary[:cls._struct().size]))

    def __init__(self, capsuleGuid, headerSize, fullSize, flags):
        # TODO use UefiGuid
        self._capsuleGuid = capsuleGuid
        self._headerSize = headerSize
        self._fullSize = fullSize
        self._flags = flags

    def getSize(self):
        return self._struct().size

    def serialize(self):
        binary = self._struct().pack(self._capsuleGuid, self._headerSize, self._fullSize, self._flags)
        return binary
