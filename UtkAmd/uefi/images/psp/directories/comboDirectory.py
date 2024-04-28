from UtkAmd.uefi.images.psp.directories.comboDirectoryHeader import ComboDirectoryHeader
from UtkAmd.uefi.images.psp.directories.directory import Directory
from UtkAmd.uefi.images.psp.directories.directoryEntries.comboDirectoryEntry import ComboDirectoryEntry
from UtkBase.utility import fillBinaryTill


# Seemingly comboDirectories are 0x400 bytes large
DIRECTORY_SIZE = 0x400


class ComboDirectory(Directory):
    """
    ComboDirectory implementation,
    a directory whose entries point at other directories.
    Consists of:
    - ComboDirectoryHeader starting with b'2PSP' or b'2BHD' as signatures
    - [?] ComboDirectoryEntries

    Size reserved for hte "full" ComboDirectory seems to be 0x400 as is for all directories
    """

    @classmethod
    def signature(cls):
        return [b'2PSP', b'2BHD']

    @classmethod
    def fromBinary(cls, binary: bytes, header: ComboDirectoryHeader = None, offset: int = None, *kwargs) -> 'ComboDirectory':
        assert binary is not None, "Binary is None"

        if header is None:
            # Will assert on issues
            header = ComboDirectoryHeader.fromBinary(binary)

        directoryEntries = []
        comboEntryOffset = header.getSize()
        for index in range(header.getEntryCount()):
            dirEntry = ComboDirectoryEntry.fromBinary(binary[comboEntryOffset:])

            directoryEntries.append(dirEntry)
            comboEntryOffset += dirEntry.getSize()

        comboDirectory = cls(offset, header, directoryEntries)
        return comboDirectory

    def __init__(self, offset: int, header: ComboDirectoryHeader, directoryEntries: list[ComboDirectoryEntry]):

        self._offset = offset
        self._header = header

        self._directoryEntries = directoryEntries

    def getOffset(self) -> int:
        return self._offset

    def getDirectoryEntries(self) -> list[ComboDirectoryEntry]:
        """Get copied List of directoryEntries"""
        return self._directoryEntries.copy()

    def getSize(self) -> int:
        """Get the directories size, seemingly always 0x400"""
        return DIRECTORY_SIZE

    def getHeader(self) -> ComboDirectoryHeader:
        return self._header

    def toDict(self) -> dict[str, any]:
        return {
            "offset": self._offset,
            "header": self._header,
            "directoryEntries": self._directoryEntries
        }

    def serialize(self) -> bytes:
        binary = self._header.serialize()
        for dirEntry in self._directoryEntries:
            binary += dirEntry.serialize()

        binary = fillBinaryTill(binary, DIRECTORY_SIZE)
        return binary
