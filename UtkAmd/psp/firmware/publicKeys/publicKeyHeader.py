from utkInterfaces import Header


class PublicKeyHeader(Header):
    @classmethod
    def fromBinary(cls, binary: bytes) -> 'PublicKeyHeader':

        publicKeyExponentBits = int.from_bytes(binary[0x38:0x38 + 4], "little")
        publicKeyModulusBits = int.from_bytes(binary[0x3C:0x3C + 4], "little")

        assert publicKeyModulusBits == publicKeyExponentBits
        assert publicKeyExponentBits in [2048, 4096], "Weird bits for exponent; must be 2048 or 4096"

        assert publicKeyExponentBits & 0x3 == 0
        publicKeyExponentSize = publicKeyExponentBits >> 3

        assert publicKeyModulusBits & 0x3 == 0
        publicKeyModulusSize = publicKeyModulusBits >> 3

        return cls(binary, publicKeyExponentSize, publicKeyModulusSize)

    def __init__(self, binary: bytes, publicKeyExponentSize: int, publicKeyModulusSize: int):
        self._binary = binary
        self._publicKeyExponentSize = publicKeyExponentSize
        self._publicKeyModulusSize = publicKeyModulusSize

    def getKeyExponentSize(self) -> int:
        return self._publicKeyExponentSize

    def getKeyModulusSize(self) -> int:
        return self._publicKeyModulusSize

    def getSize(self):
        return 0x40

    def toDict(self) -> dict[str, any]:
        return {
            "publicKeyExponentSize": self._publicKeyExponentSize,
            "publicKeyModulusSize": self._publicKeyModulusSize,
            "binary": self._binary
        }

    def serialize(self) -> bytes:
        return self._binary
