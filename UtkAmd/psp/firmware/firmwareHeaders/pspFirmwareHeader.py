import struct
from ctypes import LittleEndianStructure, c_uint32, c_uint8, c_uint16, c_uint64, c_byte

from utkInterfaces import Header


class _PspHeaderStructure(LittleEndianStructure):
    """


    https://github.com/linuxboot/fiano/blob/0ad88a5434e67ab30e2851873a33c7208cfa2db8/pkg/amd/psb/psbbinary.go#L20
    """
    _fields_ = [
        ("SizeSigned", c_uint32),
        ("EncryptionOptions", c_uint32),
        ("IKEKType", c_uint8),
        ("Reserved0", c_byte * 3),
        ("EncryptionParameters", c_byte * 16),
        ("SignatureOption", c_uint32),
        ("SignatureAlgorithmID", c_uint32),
        ("SignatureParameters", c_byte * 16),
        ("CompressionOptions", c_uint32),
        ("SecurityPatchLevel", c_uint32),
        ("UncompressedImageSize", c_uint32),
        ("CompressedImageSize", c_uint32),
        ("CompressionParameters", c_uint64),
        ("ImageVersion", c_uint32),
        ("ApuFamilyID", c_uint32),
        ("FirmwareLoadAddress", c_uint32),
        ("SizeImage", c_uint32),
        ("SizeFwUnsigned", c_uint32),
        ("FirmwareSplitAddress", c_uint32),
        ("Reserved", c_byte * 4),
        ("FwType", c_uint8),
        ("FwSubType", c_uint8),
        ("Reserved1", c_uint16),
        ("EncryptionKey", c_byte * 16),
        ("SigningInfo", c_byte * 16),
        ("FwSpecificData", c_byte * 32),
        # ("DebugEncKey", c_byte * 16),          # this collides by at least 4 bytes with the sha256Checksum
        ("DebugEncKey", c_byte * 12),            # So with that, this is probably not an encryption key
        # ("Unknown16Byte", c_byte * 16),
        ("Sha256Checksum", c_byte * 32),        # Definitively the checksum!
        # ("Reserved2", c_byte * 12)            # the checksum is followed by 12 0 bytes. But putting it here like this, somehow still leaves 4 bytes. Making it 16, explodes the buffer, I call bullshit.
    ]


class PspFirmwareHeader(Header):
    """
    Header object /structure for Platform Secure Processor firmware

    References:
    https://github.com/coreboot/coreboot/blob/master/Documentation/soc/amd/psp_integration.md

    """

    @classmethod
    def _struct(cls) -> struct:
        return struct.Struct("<16s 4s")     # Zeros - Magic:   signedSize, encrypted

    @classmethod
    def fromBinary(cls, binary: bytes) -> 'PspFirmwareHeader':
        structBinary = binary[:cls._struct().size]
        trailingBinary = binary[cls._struct().size:0x100]

        testBinary = binary[:0x100]
        zeros, magic = cls._struct().unpack(structBinary)
        assert magic in [b'$PS1', b'\x05\x00\x00\x00'], f"Wrong or missing psp header magic, got {magic}"

        internalStructure = _PspHeaderStructure.from_buffer_copy(trailingBinary)
        structureSize = len(bytes(internalStructure))
        trailingBinary = trailingBinary[structureSize:]

        return cls(zeros, magic, internalStructure, trailingBinary, testBinary)

    def __init__(self, zeros: bytes, magic: bytes, internalStructure: _PspHeaderStructure, trailingBinary: bytes, testBinary: bytes):
        self._zeros = zeros
        self._magic = magic

        self._internalStructure = internalStructure

        self._trailingBinary = trailingBinary

        self._testBinary = testBinary

    def getSize(self) -> int:
        """ fixed 256 bytes starting with 16 0es and then $PS1 """
        return 0x100

    def getFirmwareSigningKeyId(self) -> str:
        """
        :return: KeyId as a hex, upper string
        """
        keyId = bytes(self._internalStructure.SignatureParameters).hex().upper()
        return keyId

    def isFirmwareSigned(self) -> bool:
        """Is the firmware signed?"""
        return self._internalStructure.SignatureOption == 0x01
        sizeSignedOk = self._internalStructure.SizeSigned > 0
        #sizeImageOk = self._internalStructure.SizeImage > 0
        return sizeSignedOk

    def isFirmwareCompressed(self) -> bool:
        """Is the firmware compressed?"""
        compressedImageSizeOk = self._internalStructure.CompressedImageSize > 0
        uncompressedImageSizeOk = self._internalStructure.UncompressedImageSize > 0
        compressionOptionsOk = self._internalStructure.CompressionOptions > 0
        return compressedImageSizeOk and uncompressedImageSizeOk and compressionOptionsOk

    def getSignedSize(self) -> int:
        """
        Amount of signed bytes of data
        Does not include this headers size who needs to also be included
        :return:
        """
        return self._internalStructure.SizeSigned

    def getCompressedImageSize(self) -> int:
        """

        :return:
        """
        return self._internalStructure.CompressedImageSize

    def getUncompressedImageSize(self) -> int:
        """

        :return:
        """
        return self._internalStructure.UncompressedImageSize

    def getImageSize(self) -> int:
        return self._internalStructure.SizeImage

    def toDict(self) -> dict[str, any]:
        return {
            "magic": self._magic,

            "SizeSigned": self._internalStructure.SizeSigned,
            "EncryptionOptions": self._internalStructure.EncryptionOptions,
            "IKEKType": self._internalStructure.IKEKType,
            "Reserved0": bytes(self._internalStructure.Reserved0),
            "EncryptionParameters": bytes(self._internalStructure.EncryptionParameters),
            "SignatureOption": self._internalStructure.SignatureOption,
            "SignatureAlgorithmID": self._internalStructure.SignatureAlgorithmID,
            "SignatureParameters": bytes(self._internalStructure.SignatureParameters),
            "CompressionOptions": self._internalStructure.CompressionOptions,
            "SecurityPatchLevel": self._internalStructure.SecurityPatchLevel,
            "UncompressedImageSize": self._internalStructure.UncompressedImageSize,
            "CompressedImageSize": self._internalStructure.CompressedImageSize,
            "CompressionParameters": self._internalStructure.CompressionParameters,
            "ImageVersion": self._internalStructure.ImageVersion,
            "ApuFamilyID": self._internalStructure.ApuFamilyID,
            "FirmwareLoadAddress": self._internalStructure.FirmwareLoadAddress,
            "SizeImage": self._internalStructure.SizeImage,
            "SizeFwUnsigned": self._internalStructure.SizeFwUnsigned,
            "FirmwareSplitAddress": self._internalStructure.FirmwareSplitAddress,
            "Reserved": bytes(self._internalStructure.Reserved),
            "FwType": self._internalStructure.FwType,
            "FwSubType": self._internalStructure.FwSubType,
            "Reserved1": self._internalStructure.Reserved1,
            "EncryptionKey": bytes(self._internalStructure.EncryptionKey),
            "SigningInfo": bytes(self._internalStructure.SigningInfo),
            "FwSpecificData": bytes(self._internalStructure.FwSpecificData),
            "DebugEncKey": bytes(self._internalStructure.DebugEncKey),
            "Sha256Checksum": bytes(self._internalStructure.Sha256Checksum),
            "trailingBinary": self._trailingBinary
        }

    def serialize(self) -> bytes:
        outputBinary = self._struct().pack(self._zeros, self._magic)
        internalStructure = bytes(self._internalStructure)
        outputBinary += internalStructure
        outputBinary += self._trailingBinary
        return outputBinary
