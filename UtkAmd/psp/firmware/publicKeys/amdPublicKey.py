from cryptography.hazmat.primitives.asymmetric import rsa

from UtkAmd.psp.firmware.publicKeys.publicKey import PublicKey
from UtkAmd.psp.firmware.publicKeys.publicKeyHeader import PublicKeyHeader
from UtkAmd.psp.firmwareTypes import FirmwareType


class AmdPublicKey(PublicKey):
    """
    Class for AMD Public keys as they are type 0x00 in PSP firmware structures.
    """

    def __init__(self, offset: int, binary: bytes, firmwareType: FirmwareType, header: PublicKeyHeader = None, rsaPublicKey: rsa.RSAPublicKey = None, signature=None):
        assert firmwareType == FirmwareType.AMD_PUBLIC_KEY, "AMD Public Key is not of type 0x00; Got {}, {}".format(firmwareType.value, firmwareType.name)
        assert signature is None, "AMD Public keys are not supposed to be signed"
        assert header.getKeyIdString() == header.getCertifyingIdString(), "AMD Public keys KeyID must match CertifyingID"

        super().__init__(offset, binary, firmwareType, header, rsaPublicKey, signature)

        if header.getKeyUsage() != 0:
            raise ValueError("Invalid KeyUsage in header for AMD Public Key")
