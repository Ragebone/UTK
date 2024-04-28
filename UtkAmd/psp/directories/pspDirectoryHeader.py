import struct

from UtkAmd.psp.directories.directoryHeader import DirectoryHeader


class PspDirectoryHeader(DirectoryHeader):
    """
    Common header implementation for PSP and Bios directories.
    """

    @classmethod
    def _struct(cls) -> struct:
        """
        signature:  4 bytes
        checksum,
        totalEntries,
        reserved
        """
        return struct.Struct('<4s I I I')

    @classmethod
    def fromBinary(cls, binary: bytes) -> 'PspDirectoryHeader':
        assert binary is not None, "None as binary"
        return cls(*cls._struct().unpack(binary[:cls._struct().size]))

    def __init__(self, signature: bytes = None, checksum: int = 0x00, count: int = 0, reserved: int = 0x00):
        # TODO properly sanitize those.
        self._signature = signature
        self._checksum = checksum
        self._count = count
        self._reserved = reserved

        self._directorySize = (reserved & 0x3FF) << 12

    def getEntryCount(self) -> int:
        return self._count

    def getSize(self):
        return self._struct().size

    def getSignature(self) -> bytes:
        return self._signature

    def getDirectorySize(self) -> int:
        return self._directorySize

    def toDict(self) -> dict[str, any]:
        return {
            "signature": self._signature,
            "checksum": self._checksum,
            "count": self._count,
            "reserved": self._reserved,
            "directorySize": self._directorySize,
        }

    def serialize(self):
        return self._struct().pack(
            self._signature,
            self._checksum,
            self._count,
            self._reserved
        )
