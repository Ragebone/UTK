import struct

from UtkAmd.uefi.images.psp.directories.directoryEntries.biosTypeAttribute import BiosTypeAttribute
from UtkAmd.uefi.images.psp.directories.directoryEntries.directoryEntry import TypedDirectoryEntry


class BiosDirectoryEntry(TypedDirectoryEntry):
    """
    Implementation for the Directory-Entry used in Bios-Directories
    """

    @classmethod
    def _struct(cls) -> struct:
        """
        Binary for the BiosTypeAttribute,
        Entry Size,
        Entry Location,
        Entry Destination
        """
        return struct.Struct('<4s I Q Q')

    @classmethod
    def fromBinary(cls, binary: bytes) -> 'BiosDirectoryEntry':
        assert binary is not None, "None as binary"
        assert len(binary) >= cls._struct().size, "Binary to short for a BiosDirectoryEntry\n{}".format(binary)
        DIR_ENTRY_BINARY = binary[:cls._struct().size]
        typeBinary, size, location, destination = cls._struct().unpack(DIR_ENTRY_BINARY)
        biosTypeAttribute: BiosTypeAttribute = BiosTypeAttribute.fromBinary(typeBinary)
        return cls(biosTypeAttribute, size, location, destination)

    def __init__(self, typeAttribute: BiosTypeAttribute, size: int, location: int, destination: int):
        self._typeAttribute: BiosTypeAttribute = typeAttribute
        self._entrySize = size
        self._entryLocation = location
        self._entryDestination = destination

        # None FW Attributes
        self._pointEntry = False

    def getEntrySize(self) -> int:
        """Get the size of the Entry (ImageElement) this BiosDirectoryEntry references / points at"""
        return self._entrySize

    def getEntryType(self) -> int:
        return self._typeAttribute.getEntryType()

    def getEntryLocation(self) -> int:
        return self._entryLocation

    def setAsPointEntry(self, isPointEntry: bool = True) -> None:
        self._pointEntry = isPointEntry

    def isPointEntry(self) -> bool:
        return self._pointEntry

    def getSize(self) -> int:
        """Get the size of this BiosDirectoryEntry"""
        return BiosDirectoryEntry._struct().size

    def toDict(self) -> dict[str, any]:
        return {
            "typeAttribute": self._typeAttribute,
            "entrySize": self._entrySize,
            "entryLocation": self._entryLocation,
            "destination": self._entryDestination
        }

    def serialize(self) -> bytes:
        return BiosDirectoryEntry._struct().pack(
            self._typeAttribute.serialize(),
            self._entrySize,
            self._entryLocation,
            self._entryDestination
        )
