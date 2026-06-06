from ctypes import LittleEndianStructure, c_bool, c_uint16, c_uint32, c_byte

from UtkAmd.utkAmdInterfaces import UtkAMD
from utkInterfaces import Header


class _SecurityFeatures(LittleEndianStructure):
    """

    """
    _fields_ = [
        ("DISABLE_BIOS_KEY_ANTI_ROLLBACK", c_bool, 1),
        ("DISABLE_AMD_BIOS_KEY_USE", c_bool, 1),
        ("DISABLE_SECURE_DEBUG_UNLOCK", c_bool, 1),
        ("reserved", c_uint16, 12)
    ]

    def toDict(self) -> dict[str, any]:
        return {
            "DISABLE_BIOS_KEY_ANTI_ROLLBACK": self.DISABLE_BIOS_KEY_ANTI_ROLLBACK,
            "DISABLE_AMD_BIOS_KEY_USE": self.DISABLE_AMD_BIOS_KEY_USE,
            "DISABLE_SECURE_DEBUG_UNLOCK": self.DISABLE_SECURE_DEBUG_UNLOCK,
            "reserved": self.reserved,
        }


class PublicKeyHeader(LittleEndianStructure, Header, UtkAMD):
    """
    PSPTOOL sais:
    SEV spec B.1

    I had to piece this together myself though.
    It gets pretty obvious when looking at the binary
    """
    _fields_ = [
        ("_version", c_uint32),                      # 0 - 3
        ("_keyId", c_byte * 16),                     # 4 - 19
        ("_certifyingId", c_byte * 16),              # 20 - 35
        ("_keyUsage", c_uint32),                     # 36 - 39
        ("_security_features", _SecurityFeatures),   # 40 - 43
        ("_reserved", c_byte * 12),                  # 44 - 55
        ("_exponentBits", c_uint32),                 # 56 - 59
        ("_modulusBits", c_uint32),                  # 60 - 63
    ]

    @classmethod
    def fromBinary(cls, binary: bytes) -> 'PublicKeyHeader':
        headerBinary = binary[:0x40]
        assert len(headerBinary) == 0x40, "To few bytes for PublicKeyHeader, got: {}".format(binary)

        publicKeyHeader = cls.from_buffer_copy(headerBinary)

        assert publicKeyHeader._modulusBits == publicKeyHeader._exponentBits
        assert publicKeyHeader._exponentBits in [2048, 4096], "Weird bits for exponent; must be 2048 or 4096"
        assert publicKeyHeader._exponentBits & 0x3 == 0
        assert publicKeyHeader._modulusBits & 0x3 == 0

        return publicKeyHeader

    def getKeyExponentSize(self) -> int:
        return self._exponentBits >> 3

    def getKeyModulusSize(self) -> int:
        return self._modulusBits >> 3

    def getSize(self) -> int:
        return 0x40

    def getCertifyingIdString(self) -> str:
        return bytes(self._certifyingId).hex().upper()

    def getKeyId(self) -> bytes:
        return bytes(self._keyId)

    def getKeyIdString(self) -> str:
        return self.getKeyId().hex().upper()

    def getKeyUsage(self) -> int:
        return self._keyUsage

    def toDict(self) -> dict[str, any]:
        return {
            "version": self._version,
            "keyId": bytes(self._keyId),
            "certifyingId": bytes(self._certifyingId),
            "keyUsage": self._keyUsage,
            "security_features": self._security_features.toDict(),
            "reserved": bytes(self._reserved),
            "exponentBits": self._exponentBits,
            "modulusBits": self._modulusBits,
        }

    def serialize(self) -> bytes:
        return bytes(self)
