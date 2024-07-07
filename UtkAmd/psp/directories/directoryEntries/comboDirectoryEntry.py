import struct

from UtkAmd.psp.directories.directoryEntries.directoryEntry import PointDirectoryEntry
from UtkAmd.psp.directories.directoryEntries.entryReference import EntryReference


class ComboDirectoryEntry(PointDirectoryEntry):
    """
    Implementation of a Directory-Entry as it is used in Combo-Directories

    Combo directory entries are always pointDirectoryEntries because ComboDirectories have no 'content' so to speak.
    So any location referenced / pointed at is outside the Directory bounds and thereby a PointDirectoryEntry
    """

    @classmethod
    def _struct(cls) -> struct.Struct:
        return struct.Struct('<IIQ')

    @classmethod
    def fromBinary(cls, binary: bytes) -> 'ComboDirectoryEntry':
        assert binary is not None, "None as binary"
        return cls(*cls._struct().unpack(binary[:cls._struct().size]))

    def __init__(self, idSelect, chipId, directoryAddress):
        self._idSelect = idSelect
        self._chipId = chipId

        self._directoryReference: EntryReference = EntryReference.fromOffset(directoryAddress)

    def isPointEntry(self) -> bool:
        """Always True because ComboDirectoryEntry"""
        return True

    def getEntryLocation(self) -> int:
        return self._directoryReference.getAbsoluteOffset()

    def getSize(self):
        return ComboDirectoryEntry._struct().size

    def toDict(self) -> dict[str, any]:
        return {
            "idSelect": self._idSelect,
            "chipId": self._chipId,
            "directoryReference": self._directoryReference
        }

    def serialize(self) -> bytes:
        return ComboDirectoryEntry._struct().pack(self._idSelect, self._chipId, self._directoryReference.getOffset())
