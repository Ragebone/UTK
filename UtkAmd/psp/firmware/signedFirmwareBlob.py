import logging
import zlib

from UtkAmd.psp.firmware.firmwareHeaders.firmwareHeaderFactory import FirmwareHeaderFactory
from UtkAmd.psp.firmware.firmwareHeaders.pspFirmwareHeader import PspFirmwareHeader
from UtkAmd.psp.firmware.firmwareInterface import Firmware
from UtkAmd.psp.firmware.publicKeys.keyMap import KeyMap
from UtkAmd.psp.firmware.publicKeys.publicKey import PublicKey
from UtkAmd.psp.firmwareTypes import FirmwareType
from UtkAmd.utkAmdInterfaces import UtkAMD
from UtkBase.utility import fillBinaryTill, diffBinary
from UtkCommon.interfaces.reference import Reference


def verifySha256Checksum(body: bytes) -> bytes:
    """

    :param body:
    :return:
    """
    from hashlib import sha256
    return bytes(sha256(body))


class SignedFirmwareBlob(Firmware, UtkAMD):
    """
    Generic class for Signed AMD Zen specific firmware.
    """

    @classmethod
    def fromBinary(cls, binary: bytes, header: PspFirmwareHeader = None, offset: int = 0, firmwareType: FirmwareType = None) -> 'Firmware':
        """
        Construct a FirmwareBlob from the given binary
        The given binary has to contain everything including the header.
        Given Header objects will be ignored at this point

        NOTE the firmwareType is an unusual addition to the function.
        Firmware Type corresponds to the "Type" number defined by AMD.
        """

        TOTAL_SIZE = len(binary)

        if header is None:
            header = FirmwareHeaderFactory.fromBinary(binary)

        if header is None:
            # TODO more info printing for this extreme case that might never happen
            raise ValueError(f"Signed firmware needs a Header")

        assert header.isFirmwareSigned(), "Unsigned firmware passed to SignedFirmware class"

        body_data_end = header.getRomSize()

        if body_data_end == 0:
            body_data_end = TOTAL_SIZE

        if body_data_end > TOTAL_SIZE:
            body_data_end = TOTAL_SIZE

        assert body_data_end <= TOTAL_SIZE, "More signed data then actual bytes in firmware"

        signatureSize = {
            0x00: 0x100,
            0x01: 0x200,        # for a test only. 0x01 is not really defined in a sense
            0x02: 0x200,
            0x03: 0x200,        # Found in an X570 gigabyte.TODO verify the actual size, i just guessed 0x200
        }.get(header.getSecurityPatchLevel())

        SIGNATURE_START = body_data_end - signatureSize

        BODY = binary[header.getSize():SIGNATURE_START]

        signature_binary = binary[SIGNATURE_START:]

        assert len(signature_binary) in [256, 512], "Signature of unexpected size"

        return cls(binary, offset, TOTAL_SIZE, firmwareType, header, BODY, signature_binary)

    def isSignatureValid(self) -> bool:
        """

        :return:
        """
        keys = KeyMap.keys
        usedKeyId = self._header.getFirmwareSigningKeyId()
        key: PublicKey = keys.get(usedKeyId, None)
        if key is None:
            raise ValueError(f"Key {usedKeyId} not found in KeyMap")

        SIGNED_BINARY = self._header.serialize()
        if self._header.isFirmwareCompressed():
            try:
                SIGNED_BINARY += zlib.decompress(self._maybe_signed_body)
            except:
                logging.error("Zlib decompression Failed")
                return False
        else:
            SIGNED_BINARY += self._maybe_signed_body

        valid = key.verify(self._signature_binary, SIGNED_BINARY)
        return valid

    def __init__(self, binary, offset: int, total_size: int, firmwareType: FirmwareType, header: PspFirmwareHeader, body: bytes, signature_binary: bytes):
        super().__init__()
        self._binary = binary
        assert firmwareType is not None, "firmwareType can't be None"
        self._offset = offset
        self._size = total_size
        self._firmwareType = firmwareType

        self._header: PspFirmwareHeader = header
        self._maybe_signed_body: bytes = body
        self._signature_binary: bytes = signature_binary

        self._references: list[Reference] = []

    def registerReference(self, reference: Reference) -> None:
        self._references.append(reference)

    def getReferences(self) -> list[Reference]:
        return self._references

    def getSize(self) -> int:
        return self._size

    def getOffset(self) -> int:
        return self._offset

    def toDict(self) -> dict[str, any]:
        return {
            "offset": self._offset,
            "size": self._size,
            "type": self._firmwareType,
            "header": self._header,
            "data": self._maybe_signed_body,
            "signature": self._signature_binary
        }

    def serialize(self) -> bytes:
        outputBinary = self._header.serialize()
        outputBinary += self._maybe_signed_body
        outputBinary += self._signature_binary

        if len(outputBinary) == self._size:
            return outputBinary

        outputBinary = fillBinaryTill(outputBinary, self._size)

        assert diffBinary(outputBinary, self._binary), "binary missmatch to unmodified copy"

        return outputBinary
