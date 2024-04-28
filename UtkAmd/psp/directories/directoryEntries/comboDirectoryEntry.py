import struct

from UtkAmd.psp.directories.directoryEntries.directoryEntry import PointDirectoryEntry


class ComboDirectoryEntry(PointDirectoryEntry):
    """
    Implementation of a Directory-Entry as it is used in Combo-Directories

    Combo directory entries are always pointDirectoryEntries because ComboDirectories have no 'content' so to speak.
    So any location referenced / pointed at is outside the Directory bounds and thereby a PointDirectoryEntry
    """

    @classmethod
    def _struct(cls):
        return struct.Struct('<IIQ')

    @classmethod
    def fromBinary(cls, binary: bytes):
        assert binary is not None, "None as binary"
        return cls(*cls._struct().unpack(binary[:cls._struct().size]))

    def __init__(self, idSelect, chipId, directoryAddress):
        self._idSelect = idSelect
        self._chipId = chipId

        self._directoryAddress = directoryAddress

    def isPointEntry(self):
        """Always True because ComboDirectoryEntry"""
        return True

    def getEntryLocation(self):
        return self._directoryAddress

    def getSize(self):
        return ComboDirectoryEntry._struct().size

    def toDict(self) -> dict[str, any]:
        return {
            "idSelect": self._idSelect,
            "chipId": self._chipId,
            "directoryAddress": self._directoryAddress
        }

    def serialize(self):
        return ComboDirectoryEntry._struct().pack(self._idSelect, self._chipId, self._directoryAddress)
