from UtkAmd.psp.addressMode import AddressMode
from UtkAmd.psp.directories.directory import ContentDirectory
from UtkAmd.psp.directories.directoryEntries.pspDirectoryEntry import PspDirectoryEntry
from UtkAmd.psp.directories.directoryEntries.softFuseChain import SoftFuseChain


class PspDirectory(ContentDirectory):
    """
    The specific directory implementation for PSP related firmware-items.

    The Header must start with b'$PSP' or b'$PL2'

    For more implementation details, look at the directory.py  ContentDirectory
    """

    @classmethod
    def _buildDirectoryEntry(cls, binary: bytes, addressMode: AddressMode = None) -> PspDirectoryEntry:
        """

        :param binary:
        :return:
        """
        dirEntryType = binary[0]                # First byte is Type
        if dirEntryType == 0x0B:
            return SoftFuseChain.fromBinary(binary)
        return PspDirectoryEntry.fromBinary(binary, addressMode)
