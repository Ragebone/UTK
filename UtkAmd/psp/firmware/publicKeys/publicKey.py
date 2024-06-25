from cryptography.hazmat.primitives.asymmetric import rsa

from UtkAmd.psp.firmware.firmwareBlob import FirmwareBlob
from UtkAmd.psp.firmware.publicKeys.publicKeyHeader import PublicKeyHeader
from UtkAmd.psp.firmwareTypes import FirmwareType
from utkInterfaces import Header


class PublicKey(FirmwareBlob):
    """
    Class for AMD Public keys as they are type 0x00 in PSP firmware structures.
    """

    @classmethod
    def fromBinary(cls, binary: bytes, header: Header = None, offset: int = 0, firmwareType: FirmwareType = None) -> 'PublicKey':
        """
        Construct a UtkAmd related PSP Public key from the given binary.
        """
        assert header is None, "AMD Public Keys should never have a normal $PS1 header"
        assert firmwareType is not None, "FirmwareType must not be None"
        assert firmwareType == FirmwareType.AMD_PUBLIC_KEY, "AMD Public Key is not of type 0x00; Got {}".format(
            firmwareType)

        header = PublicKeyHeader.fromBinary(binary[:0x40])

        KEY_EXPONENT_SIZE = header.getKeyExponentSize()
        KEY_MODULUS_SIZE = header.getKeyModulusSize()

        KEY_SIZE = KEY_EXPONENT_SIZE + KEY_MODULUS_SIZE
        KEY_START = header.getSize()
        KEY_END = KEY_START + KEY_SIZE

        keyBinary = binary[KEY_START:KEY_END]

        exponentBinary = keyBinary[:KEY_EXPONENT_SIZE]
        modulusBinary = keyBinary[KEY_EXPONENT_SIZE:KEY_END]

        publicKeyExponent = int.from_bytes(exponentBinary, "little")
        publicKeyModulus = int.from_bytes(modulusBinary, "little")
        assert publicKeyExponent == 0x10001, "Unexpected public key exponent {}".format(hex(publicKeyExponent))

        # TODO  if there is anything left in the binary behind the exponent and modulus, that is then the signature
        # TODO signature must be of sizes 0x100 or 0x200

        rsaPublicKey = rsa.RSAPublicNumbers(publicKeyExponent, publicKeyModulus).public_key()

        signatureBinary = binary[KEY_END:]

        signature = None

        if len(signatureBinary) > 0:
            signature = signatureBinary

        return cls(offset, keyBinary, firmwareType, header, rsaPublicKey, signature)

    def __init__(self, offset: int, binary: bytes, firmwareType: FirmwareType, header: PublicKeyHeader = None,
                 rsaPublicKey: rsa.RSAPublicKey = None, signature=None):
        assert firmwareType is not None, "firmwareType must not be None"
        super().__init__(offset, binary, firmwareType)

        self._header = header
        self._rsaPublicKey = rsaPublicKey
        self._signature = signature

    def getSize(self) -> int:
        return len(self._binary) + self._header.getSize()

    def toDict(self) -> dict[str, any]:

        return {
            "offset": self._offset,
            "firmwareType": self._firmwareType,
            "binary": self._binary,
            "header": self._header,
            # "rsaPublicKey": self._rsaPublicKey,
            "signature": self._signature
        }

    def serialize(self) -> bytes:
        return self._header.serialize() + self._binary
