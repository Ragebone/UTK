from cryptography.hazmat.primitives.asymmetric import rsa

from UtkAmd.psp.firmware.publicKeys.publicKey import PublicKey
from UtkAmd.psp.firmware.publicKeys.publicKeyHeader import PublicKeyHeader
from UtkAmd.psp.firmwareTypes import FirmwareType


class OemPublicKey(PublicKey):
    """
    Class for OEM Public keys as they are type 0x05 in PSP firmware structures.
    """

    def __init__(self, offset: int, binary: bytes, firmwareType: FirmwareType, header: PublicKeyHeader = None, rsaPublicKey: rsa.RSAPublicKey = None, signature=None):
        # assert firmwareType == FirmwareType.OEM_PSP_FW_PUBLIC_KEY, "OEM Public Key is not of type 0x0A; Got {}, {}".format(firmwareType.value, firmwareType.name)

        super().__init__(offset, binary, firmwareType, header, rsaPublicKey, signature)

        # if header.getKeyUsage() != 0:
        #    raise ValueError("Invalid KeyUsage in header for AMD Public Key")

