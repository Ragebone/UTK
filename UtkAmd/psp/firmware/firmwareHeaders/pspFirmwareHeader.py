import struct
from ctypes import c_uint32, c_uint8, c_uint16, c_uint64, c_byte

from UtkCommon.implementations.structures import leStructure
from UtkCommon.interfaces.header import Header


class _PspHeaderStructure(leStructure):
    """


    https://github.com/linuxboot/fiano/blob/0ad88a5434e67ab30e2851873a33c7208cfa2db8/pkg/amd/psb/psbbinary.go#L20
    total of 188 / 0xBC bytes + 48 padding at the end
    """
    _fields_ = [                                        # decimal
        ("SizeSigned", c_uint32),                       # KeyStoreHeader body_size
        ("EncryptionOptions", c_uint32),
        ("IKEKType", c_uint8),
        ("Reserved0", c_byte * 3),
        ("EncryptionParameters", c_byte * 16),          # 12
        ("SignatureOption", c_uint32),                  # 28; No, this is not what the PSP tool calls signature_type at 0x34 to 0x38
        ("SignatureAlgorithmID", c_uint32),             # 32
        ("UnkownSignatureParameters", c_byte * 12),     # 36
        ("Signed", c_uint32),                           # 48
        ("CompressionOptions", c_uint32),               # 52        signature type
        ("SecurityPatchLevel", c_uint32),               # 56        signature fingerprint keyStoreHeader: certifying_id
        ("UncompressedImageSize", c_uint32),            # 60
        ("CompressedImageSize", c_uint32),              # 64
        ("CompressionParameters", c_uint64),            # 68        at 72 compressed uint32
        ("ImageVersion", c_uint32),                     # 76
        ("ApuFamilyID", c_uint32),                      # 80
        ("FirmwareLoadAddress", c_uint32),              # 84
        ("SizeImage", c_uint32),                        # 88
        ("SizeFwUnsigned", c_uint32),                   # 92
        ("FirmwareSplitAddress", c_uint32),             # 96
        ("Reserved", c_byte * 4),                       # 100
        ("FwType", c_uint8),                            # 104
        ("FwSubType", c_uint8),                         # 105
        ("Reserved1", c_uint16),                        # 106
        ("RomSize", c_uint32),                          # 108       KeyStoreHeader: packed_size
        ("EncryptionKey", c_byte * 12),                 # 112
        ("SigningInfo", c_byte * 16),                   # 124       KeyStoreHader: 4bytes keystore_type either 0 or [0x50, 0x51]
        ("FwSpecificData", c_byte * 32),                #
        # ("DebugEncKey", c_byte * 16),                 # this collides by at least 4 bytes with the sha256Checksum
        ("DebugEncKey", c_byte * 12),                   # So with that, this is probably not an encryption key
        # ("Unknown16Byte", c_byte * 16),
        ("Sha256Checksum", c_byte * 32),                # Definitively the checksum, but of what?
        # ("Reserved2", c_byte * 12)                    # the checksum is followed by 12 0 bytes. But putting it here like this, somehow still leaves 4 bytes. Making it 16, explodes the buffer, I call bullshit.
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

    @classmethod
    def fromJson(cls, file_path: str) -> 'PspFirmwareHeader':
        """
        Reconstruct from JSON file.
        Keys are matched case-insensitively with typo suggestions.
        """
        from UtkBase.utility import readJson

        data = readJson(file_path)

        magic = bytes.fromhex(data['magic'])
        zeros = b'\x00' * 16
        trailingBinary = bytes.fromhex(data.get('trailingBinary', '')) or b''

        internalStructure = _PspHeaderStructure.fromDict(data)
        testBinary = bytes(internalStructure).ljust(0x100, b'\x00')

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

    def getRomSize(self)-> int:
        return self._internalStructure.RomSize

    def getFirmwareSigningKeyId(self) -> str:
        """
        :return: KeyId as a hex, upper string
        """
        keyId = bytes(self._internalStructure.SignatureParameters).hex().upper()
        return keyId

    def isFirmwareSigned(self) -> bool:
        """Is the firmware signed?"""
        return self._internalStructure.Signed > 0x00
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

    def getSecurityPatchLevel(self) -> int:
        return self._internalStructure.SecurityPatchLevel

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
            **self._internalStructure.toDict(),
            "trailingBinary": self._trailingBinary,
        }

    # def toDict(self) -> dict[str, any]:
    #     return {
    #         "magic": self._magic,
    #
    #         "SizeSigned": self._internalStructure.SizeSigned,
    #         "EncryptionOptions": self._internalStructure.EncryptionOptions,
    #         "IKEKType": self._internalStructure.IKEKType,
    #         "Reserved0": bytes(self._internalStructure.Reserved0),
    #         "EncryptionParameters": bytes(self._internalStructure.EncryptionParameters),
    #         "SignatureOption": self._internalStructure.SignatureOption,
    #         "SignatureAlgorithmID": self._internalStructure.SignatureAlgorithmID,
    #         "SignatureParameters": bytes(self._internalStructure.SignatureParameters),
    #         "CompressionOptions": self._internalStructure.CompressionOptions,
    #         "SecurityPatchLevel": self._internalStructure.SecurityPatchLevel,
    #         "UncompressedImageSize": self._internalStructure.UncompressedImageSize,
    #         "CompressedImageSize": self._internalStructure.CompressedImageSize,
    #         "CompressionParameters": self._internalStructure.CompressionParameters,
    #         "ImageVersion": self._internalStructure.ImageVersion,
    #         "ApuFamilyID": self._internalStructure.ApuFamilyID,
    #         "FirmwareLoadAddress": self._internalStructure.FirmwareLoadAddress,
    #         "SizeImage": self._internalStructure.SizeImage,
    #         "SizeFwUnsigned": self._internalStructure.SizeFwUnsigned,
    #         "FirmwareSplitAddress": self._internalStructure.FirmwareSplitAddress,
    #         "Reserved": bytes(self._internalStructure.Reserved),
    #         "FwType": self._internalStructure.FwType,
    #         "FwSubType": self._internalStructure.FwSubType,
    #         "Reserved1": self._internalStructure.Reserved1,
    #         "EncryptionKey": bytes(self._internalStructure.EncryptionKey),
    #         "SigningInfo": bytes(self._internalStructure.SigningInfo),
    #         "FwSpecificData": bytes(self._internalStructure.FwSpecificData),
    #         "DebugEncKey": bytes(self._internalStructure.DebugEncKey),
    #         "Sha256Checksum": bytes(self._internalStructure.Sha256Checksum),
    #         "trailingBinary": self._trailingBinary
    #     }

    def serialize(self) -> bytes:
        outputBinary = self._struct().pack(self._zeros, self._magic)
        internalStructure = bytes(self._internalStructure)
        outputBinary += internalStructure
        outputBinary += self._trailingBinary
        return outputBinary
