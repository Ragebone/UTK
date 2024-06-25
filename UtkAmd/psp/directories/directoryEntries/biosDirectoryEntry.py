import struct

from UtkAmd.psp.addressMode import AddressMode
from UtkAmd.psp.directories.directoryEntries.biosTypeAttribute import BiosTypeAttribute
from UtkAmd.psp.directories.directoryEntries.directoryEntry import TypedDirectoryEntry
from UtkAmd.psp.directories.directoryEntries.entryReference import EntryReference
from UtkAmd.psp.firmwareTypes import FirmwareType


class BiosDirectoryEntry(TypedDirectoryEntry):
    """
    Implementation for the Directory-Entry used in Bios-Directories
    """

    @classmethod
    def _struct(cls) -> struct:
        """
        FirmwareType int
        Binary for the BiosTypeAttribute,
        Entry Size,
        Entry Location,
        Entry Destination
        """
        return struct.Struct('<B3s I Q Q')

    @classmethod
    def fromBinary(cls, binary: bytes,  addressMode: AddressMode = None) -> 'BiosDirectoryEntry':
        assert binary is not None, "None as binary"
        assert len(binary) >= cls._struct().size, "Binary to short for a BiosDirectoryEntry\n{}".format(binary)
        DIR_ENTRY_BINARY = binary[:cls._struct().size]
        typeInt, attributeBinary, size, location, destination = cls._struct().unpack(DIR_ENTRY_BINARY)
        biosTypeAttribute: BiosTypeAttribute = BiosTypeAttribute.fromBinary(attributeBinary)
        return cls(typeInt, biosTypeAttribute, size, location, destination, addressMode)

    def __init__(self, firmwareTypeInt: int, typeAttribute: BiosTypeAttribute, size: int, location: int, destination: int, addressMode: AddressMode = None):
        self._firmwareType: FirmwareType = FirmwareType(firmwareTypeInt)
        self._typeAttribute: BiosTypeAttribute = typeAttribute
        self._entrySize = size
        self._entryReference: EntryReference = EntryReference.fromOffset(location, addressMode)
        self._entryDestination = destination

        # None FW Attributes
        self._pointEntry = False

    def getEntrySize(self) -> int:
        """Get the size of the Entry (ImageElement) this BiosDirectoryEntry references / points at"""
        return self._entrySize

    def getEntryType(self) -> FirmwareType:
        return self._firmwareType

    def getEntryLocation(self) -> int:
        return self._entryReference.getAbsoluteOffset()

    def setAsPointEntry(self, isPointEntry: bool = True) -> None:
        self._pointEntry = isPointEntry

    def isPointEntry(self) -> bool:
        return self._pointEntry

    def getSize(self) -> int:
        """Get the size of this BiosDirectoryEntry"""
        return BiosDirectoryEntry._struct().size

    def toDict(self) -> dict[str, any]:
        return {
            "firmwareType": self._firmwareType,
            "typeAttribute": self._typeAttribute,
            "entrySize": self._entrySize,
            "entryReference": self._entryReference,
            "destination": self._entryDestination
        }

    def serialize(self) -> bytes:
        return BiosDirectoryEntry._struct().pack(
            self._firmwareType.value,
            self._typeAttribute.serialize(),
            self._entrySize,
            self._entryReference.getOffset(),
            self._entryDestination
        )
