import struct

from UtkAmd.psp.addressMode import AddressMode
from UtkAmd.psp.directories.directoryEntries.directoryEntry import TypedDirectoryEntry, DirectoryEntry
from UtkAmd.psp.directories.directoryEntries.entryReference import EntryReference
from UtkAmd.psp.directories.directoryEntries.romId import RomId
from UtkAmd.psp.directories.directoryEntries.softFuseChain import SoftFuseChain
from UtkAmd.psp.directories.directoryEntries.writable import Writeable
from UtkAmd.psp.firmwareTypes import FirmwareType


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
    def _buildDirectoryEntry(cls, binary: bytes) -> 'DirectoryEntry':
        dirEntryTypeInt = binary[0]                # First byte is Type value as Int
        dirEntryType: FirmwareType = FirmwareType(dirEntryTypeInt)

        if dirEntryType == FirmwareType.AMD_SOFT_FUSE_CHAIN_01:
            softFuseChain = SoftFuseChain.fromBinary(binary)
            return softFuseChain

        dirEntry = PspDirectoryEntry.fromBinary(binary)
        return dirEntry

    @classmethod
    def fromBinary(cls, binary: bytes, addressMode: AddressMode = None) -> 'PspDirectoryEntry':
        assert binary is not None, "None as binary"
        return cls(*cls._struct().unpack(binary[:cls._struct().size]), addressMode)

    def __init__(self, entryType: int, subProgram: int, byteGroup: int, entrySize: int, offset: int, addressMode: AddressMode = None):
        self._entryType: FirmwareType = FirmwareType(entryType)
        self._entrySize = entrySize
        # TODO make this a nice type thing bitfield as it is with the BiosTypeAttribute
        self._subProgram = subProgram

        self._byteGroup = byteGroup

        self._romId: RomId = RomId(byteGroup & 0x03)
        self._writeable: Writeable = Writeable(byteGroup >> 2 & 0x1)
        self._instance = byteGroup & 0x78 >> 3
        self._reserved = byteGroup & 0xFF80

        self._entryReference: EntryReference = EntryReference.fromOffset(offset, addressMode)

        self._pointEntry = False

    def setAsPointEntry(self, isPointEntry: bool = True) -> None:
        self._pointEntry = isPointEntry

    def isPointEntry(self) -> bool:
        return self._pointEntry

    def getSize(self) -> int:
        """Get structure size"""
        return PspDirectoryEntry._struct().size

    def getEntryType(self) -> FirmwareType:
        return self._entryType

    def getEntryLocation(self) -> int:
        return self._entryReference.getAbsoluteOffset()

    def getEntryReference(self) -> EntryReference:
        return self._entryReference

    def getEntrySize(self) -> int:
        """
        Get the 'Entries' size this directoryEntry points at.
        :return: Size-value stored in the directoryEntry.
        """
        return self._entrySize

    def toDict(self) -> dict[str, any]:
        # TODO   name more things here with "entry..."
        return {
            "entryType": self._entryType,
            "entrySize": self._entrySize,
            "subProgram": self._subProgram,
            "romId": self._romId,
            "writeable": self._writeable,
            "instance": self._instance,
            "reserved": self._reserved,
            "entryReference": self._entryReference
        }

    def serialize(self) -> bytes:
        # byteGroup = (self._reserved & 0xFF80) + ((self._instance << 3) & 0x78) + ((self._writeable.value & 0x1) << 2) + (self._romId.value & 0x01)

        binary = self._struct().pack(
            self._entryType.value,
            self._subProgram,
            self._byteGroup,
            self._entrySize,
            self._entryReference.getOffset()
        )

        return binary
