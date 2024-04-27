import struct
from typing import Any

from UtkAmd.uefi.images.psp.directories.directoryEntries.directoryEntry import TypedDirectoryEntry, RomId, Writeable
from UtkAmd.uefi.images.psp.directories.directoryEntries.softFuseChain import SoftFuseChain


class PspDirectoryEntry(TypedDirectoryEntry):
    """
    Implementation of the DirectoryEntries used in Psp-Directories
    """

    @classmethod
    def _struct(cls):
        """
        Uint8 EntryType as is used in all the mappings
        Uint8 subProgram
        Uint16 a bitfield for various values
        Uint32 EntrySize
        Uint64 EntryLocation
        """
        return struct.Struct('<BBHIQ')

    @classmethod
    def _buildDirectoryEntry(cls, binary: bytes) -> 'PspDirectoryEntry':
        dirEntryType = binary[0]                # First byte is Type

        if dirEntryType == 0x0B:
            softFuseChain = SoftFuseChain.fromBinary(binary)
            return softFuseChain

        dirEntry = PspDirectoryEntry.fromBinary(binary)
        return dirEntry

    @classmethod
    def fromBinary(cls, binary: bytes) -> 'PspDirectoryEntry':
        assert binary is not None, "None as binary"
        return cls(*cls._struct().unpack(binary[:cls._struct().size]))

    def __init__(self, entryType: int, subProgram: int, byteGroup: int, entrySize: int, offset: int):
        self._entryType = entryType
        self._entrySize = entrySize
        # TODO make this a nice type thing bitfield as it is with the BiosTypeAttribute
        self._subProgram = subProgram
        self._romId: RomId = RomId(byteGroup & 0x03)
        self._writeable: Writeable = Writeable(byteGroup >> 2 & 0x1)
        self._instance = byteGroup & 0x78 >> 3
        self._reserved = byteGroup & 0xFF80
        self._entryLocation = offset

        self._pointEntry = False

    def setAsPointEntry(self, isPointEntry: bool = True) -> None:
        self._pointEntry = isPointEntry

    def isPointEntry(self) -> bool:
        return self._pointEntry

    def getSize(self) -> int:
        """Get structure size"""
        return PspDirectoryEntry._struct().size

    def getEntryType(self) -> int:
        return self._entryType

    def getEntryLocation(self) -> int:
        return self._entryLocation

    def getEntrySize(self) -> int:
        """
        Get the 'Entries' size this directoryEntry points at.
        :return: Size-value stored in the directoryEntry.
        """
        return self._entrySize

    def toDict(self) -> dict[str, Any]:
        return {
            "entryType": self._entryType,
            "entrySize": self._entrySize,
            "subProgram": self._subProgram,
            "romId": self._romId,
            "writeable": self._writeable,
            "instance": self._instance,
            "reserved": self._reserved,
            "entryLocation": self._entryLocation
        }

    def serialize(self) -> bytes:
        byteGroup = (self._reserved & 0xFF80) + ((self._instance << 3) & 0x78) + ((self._writeable.value & 0x1) << 2) + (self._romId.value & 0x01)
        binary = self._struct().pack(self._entryType, self._subProgram, byteGroup, self._entrySize, self._entryLocation)
        return binary
