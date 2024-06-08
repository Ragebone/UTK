import struct

from UtkAmd.psp.addressMode import AddressMode
from UtkAmd.psp.directories.directoryHeaders.directoryHeader import DirectoryHeader
from UtkAmd.psp.directories.directoryHeaders.infoField import PspDirectoryHeaderInfoField


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
        PspDirectoryHeaderInfoField
        """
        return struct.Struct('<4s I I 4s')

    @classmethod
    def fromBinary(cls, binary: bytes) -> 'PspDirectoryHeader':
        assert binary is not None, "None as binary"

        signatureBinary, checksum, count, infoBinary = cls._struct().unpack(binary[:cls._struct().size])
        signatureBinary: bytes = signatureBinary
        signature = signatureBinary.decode('ascii')
        infoField = PspDirectoryHeaderInfoField.fromBinary(infoBinary)

        return cls(signature, checksum, count, infoField)

    def __init__(self, signature: str = None, checksum: int = 0x00, count: int = 0, infoField: PspDirectoryHeaderInfoField = None):
        self._signature = signature
        self._checksum = checksum
        self._count = count
        self._infoField = infoField

    def getEntryCount(self) -> int:
        return self._count

    def getSize(self) -> int:
        return self._struct().size

    def getSignature(self) -> str:
        return self._signature

    def getDirectorySize(self) -> int:
        return self._infoField.getMaxSize() << 12

    def getAddressMode(self) -> AddressMode:
        return self._infoField.getAddressMode()

    def toDict(self) -> dict[str, any]:
        return {
            "signature": self._signature,
            "checksum": self._checksum,
            "count": self._count,
            "infoField": self._infoField
        }

    def serialize(self) -> bytes:
        return self._struct().pack(
            self._signature.encode('ascii'),
            self._checksum,
            self._count,
            self._infoField.serialize()
        )
