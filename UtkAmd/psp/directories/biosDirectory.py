from UtkAmd.psp.directories.directory import ContentDirectory
from UtkAmd.psp.directories.directoryEntries.biosDirectoryEntry import BiosDirectoryEntry


class BiosDirectory(ContentDirectory):
    """
    The specific directory implementation for Bios related firmware-items.

    The Header must start with b'$BHD' or b'$BL2'

    For more implementation details, look at the directory.py  ContentDirectory
    """

    @classmethod
    def _buildDirectoryEntry(cls, binary: bytes) -> BiosDirectoryEntry:
        """
        Private method used in directory construction.
        Closed door - Open door; for the implementations in  Directory
        """
        return BiosDirectoryEntry.fromBinary(binary)
