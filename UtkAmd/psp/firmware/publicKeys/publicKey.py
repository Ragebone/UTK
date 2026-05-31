from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey

from UtkAmd.psp.firmware.firmwareBlob import FirmwareBlob
from UtkAmd.psp.firmware.publicKeys.keyMap import KeyMap
from UtkAmd.psp.firmware.publicKeys.publicKeyHeader import PublicKeyHeader
from UtkAmd.psp.firmwareTypes import FirmwareType


class PublicKey(FirmwareBlob):
    """
    Class for AMD Public keys as they are type 0x00 in PSP firmware structures.
    """

    def getParent(self) -> any:
        pass

    def setParent(self, parent: 'Image') -> None:
        pass

    @classmethod
    def fromBinary(cls, binary: bytes, header: PublicKeyHeader = None, offset: int = 0, firmwareType: FirmwareType = None) -> 'PublicKey':
        """
        Construct a UtkAmd related PSP Public key from the given binary.
        """
        assert firmwareType is not None, "FirmwareType must not be None"

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

        rsaPublicKey: RSAPublicKey = rsa.RSAPublicNumbers(publicKeyExponent, publicKeyModulus).public_key()

        signatureBinary = binary[KEY_END:]

        signature = None

        if len(signatureBinary) > 0:
            signature = signatureBinary

        publicKey = cls(offset, binary, firmwareType, header, rsaPublicKey, signature)
        KeyMap.addKey(header.getKeyIdString(), publicKey)
        return publicKey

    def __init__(self, offset: int, binary: bytes, firmwareType: FirmwareType, header: PublicKeyHeader = None, rsaPublicKey: rsa.RSAPublicKey = None, signature=None):
        assert firmwareType is not None, "firmwareType must not be None"
        super().__init__(offset, binary, firmwareType)

        self._header = header
        self._rsaPublicKey = rsaPublicKey
        self._signature = signature

    def verify(self, signature: bytes, signedBinary: bytes) -> bool:
        """
        Verify the signature of the given binary with this key
        :param signature:
        :param signedBinary:
        :return:
        """
        # TODO key_sizemight be shifted and hence needs to be shifted back for serialization
        keySize = self._rsaPublicKey.key_size
        if keySize == 2048:
            saltLength = 32
            hashAlgorithm = hashes.SHA256()
        elif keySize == 4096:
            saltLength = 48
            hashAlgorithm = hashes.SHA3_384()
        else:
            raise Exception(f'Unknown rsa key size: {keySize} bits!')

        cryptoPadding = padding.PSS(
            mgf=padding.MGF1(hashAlgorithm),
            salt_length=saltLength
        )

        try:
            self._rsaPublicKey.verify(
                signature,
                signedBinary,
                cryptoPadding,
                hashAlgorithm
            )
        except InvalidSignature:
            return False
        return True

    def validate(self, keyMap: dict[str, 'PublicKey']) -> bool:
        """
        Get what's needed for Validation of this Key
        :return:
        """
        certifyingId = self._header.getCertifyingIdString()
        certifyingKey = keyMap.get(certifyingId)
        if certifyingKey is None:
            # TODO logging?
            return False

        KEY_EXPONENT_SIZE = self._header.getKeyExponentSize()
        KEY_MODULUS_SIZE = self._header.getKeyModulusSize()

        KEY_SIZE = KEY_EXPONENT_SIZE + KEY_MODULUS_SIZE
        KEY_START = self._header.getSize()
        KEY_END = KEY_START + KEY_SIZE
        fullBinary = self._binary

        for count in range(100):
            signedBinary = self._binary[count:KEY_END]
            sigOk = certifyingKey.verify(self._signature, signedBinary)
            if sigOk:
                pass

        return sigOk

    def getSize(self) -> int:
        """
        :return: None
        """
        return len(self._binary)  # + self._header.getSize()

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
        return self._binary
        # TODO fix this
        outputBinary = self._header.serialize()
        outputBinary += self._binary
        if self._signature is not None:
            outputBinary += self._signature

        return outputBinary