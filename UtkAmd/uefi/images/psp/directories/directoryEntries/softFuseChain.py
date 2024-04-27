import struct
from typing import Any

from UtkAmd.uefi.images.psp.directories.directoryEntries.directoryEntry import DirectoryEntry


class SoftFuseChain(DirectoryEntry):
    """
    Occasionally referred to as a 'Secure Unlock Enable flag'.
    Only found inside PspDirectories with the Type '0x0B'.

    Unlike all other DirectoryEntries, this does not point at anything.
    Instead, the 'address' is a Bitfield with yet unknown meanings.
    """

    @classmethod
    def _struct(cls) -> struct:
        """
        Struct like any other PspDirectoryEntry.
        """

        return struct.Struct('<BBBBIQ')

    @classmethod
    def fromBinary(cls, binary: bytes):
        assert binary is not None, "None as binary"
        BINARY = binary[:cls._struct().size]
        assert len(BINARY) == cls._struct().size, "To few bytes for Soft Fuse Chain, got: {}".format(binary)

        return cls(*cls._struct().unpack(BINARY))

    def __init__(self, entryType: int, subProgram: int, romId: int, reserved: int, size: int, value: int):
        assert entryType == 0x0B, "Wrong Type for SoftFuseChain {}".format(hex(entryType))

        self._type = entryType
        self._subProgram = subProgram
        self._romId = romId
        self._reserved = reserved
        self._size = size

        # Unknown bitfield
        self._value = value

    def getSize(self) -> int:
        return self._struct().size

    def toDict(self) -> dict[str, Any]:
        return {
            "type": self._type,
            "subProgram": self._subProgram,
            "romId": self._romId,
            "reserved": self._reserved,
            "size": self._size,
            "value": self._value
        }

    def serialize(self) -> bytes:
        return self._struct().pack(self._type, self._subProgram, self._romId, self._reserved, self._size, self._value)
