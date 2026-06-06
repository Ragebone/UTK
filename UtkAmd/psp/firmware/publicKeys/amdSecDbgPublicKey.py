from cryptography.hazmat.primitives.asymmetric import rsa

from UtkAmd.psp.firmware.publicKeys.publicKey import PublicKey
from UtkAmd.psp.firmware.publicKeys.publicKeyHeader import PublicKeyHeader
from UtkAmd.psp.firmwareTypes import FirmwareType


class AmdSecDbgPublicKey(PublicKey):
    """
    Class for AMD Public keys as they are type 0x00 in PSP firmware structures.
    """

    def __init__(self, offset: int, binary: bytes, firmwareType: FirmwareType, header: PublicKeyHeader = None,
                 rsaPublicKey: rsa.RSAPublicKey = None, signature=None):

        super().__init__(offset, binary, firmwareType, header, rsaPublicKey, signature)

        assert firmwareType == FirmwareType.AMD_SEC_DBG_PUBLIC_KEY, "AMD SEC DBG Public Key is not of type 0x09; Got {}, {}".format(firmwareType.value, firmwareType.name)


