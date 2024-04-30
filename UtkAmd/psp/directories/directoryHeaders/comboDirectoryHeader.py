import struct

from UtkAmd.psp.directories.directoryHeaders.directoryHeader import DirectoryHeader
from UtkAmd.psp.directories.lookupMode import LookUpMode


class ComboDirectoryHeader(DirectoryHeader):
    """
    Header structure of Combo-Directories.
    Directories without firmware blobs.
    """

    @classmethod
    def _struct(cls) -> struct:
        """
        signature as bytes; b'2PSP' or b'2BHD',
        checksum,
        totalEntries,
        lookupMode,
        reserved as 0es
        """
        return struct.Struct('<4s I I I 16s')

    @classmethod
    def fromBinary(cls, binary: bytes) -> 'ComboDirectoryHeader':
        assert binary is not None, "None as binary"
        signature, checksum, count, lookupModeValue, reserved = cls._struct().unpack(binary[:cls._struct().size])
        lookupMode = LookUpMode(lookupModeValue)
        return cls(signature, checksum, count, lookupMode, reserved)

    def __init__(self, signature: bytes, checksum: int, count: int, lookupMode: LookUpMode, reserved: int = 0):
        assert signature in [b'2PSP', b'2BHD'], "Unexpected signature, got {}".format(signature)

        self._signature = signature
        self._checksum = checksum
        self._count = count
        self._lookupMode = lookupMode
        self._reserved = reserved

    def getEntryCount(self) -> int:
        return self._count

    def getSize(self) -> int:
        return ComboDirectoryHeader._struct().size

    def getSignature(self) -> bytes:
        return self._signature

    def toDict(self) -> dict[str, any]:
        return {
            'signature': self._signature,
            'checksum': self._checksum,
            'count': self._count,
            'lookupMode': self._lookupMode,
            'reserved': self._reserved
        }

    def serialize(self) -> bytes:
        return ComboDirectoryHeader._struct().pack(
            self._signature,
            self._checksum,
            self._count,
            self._lookupMode.value,
            self._reserved
        )
