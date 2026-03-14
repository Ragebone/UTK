import logging
import zlib

from UtkAmd.psp.firmware.firmwareHeaders.firmwareHeaderFactory import FirmwareHeaderFactory
from UtkAmd.psp.firmware.firmwareHeaders.pspFirmwareHeader import PspFirmwareHeader
from UtkAmd.psp.firmware.firmwareInterface import Firmware
from UtkAmd.psp.firmware.publicKeys.keyMap import KeyMap
from UtkAmd.psp.firmware.publicKeys.publicKey import PublicKey
from UtkAmd.psp.firmwareTypes import FirmwareType
from UtkAmd.utkAmdInterfaces import UtkAMD
from UtkBase.utility import alignOffset, binaryIsEmpty, fillBinaryTill, diffBinary
from utkInterfaces import Reference


def getSignatureFromTrailingBinary(signature_binary: bytes, securityPatchLevel: int) -> bytes:
    """

    NOTE:
    I could just figure out how long the signature is supposed to be.
    But this way here is stupid enough

    :param signature_binary:
    :return:
    """





    length = len(signature_binary)

    if length < 256:
        raise ValueError(f"Signature binary too short: {length}")

    if length == 256:
        assert securityPatchLevel == 0x00, "expected signature length indicator doesn't match the detected length"
        return signature_binary

    if length == 512:
        assert securityPatchLevel == 0x02, "expected signature length indicator doesn't match the detected length"
        return signature_binary

    if length < 512:
        # guess 256 signature length placed at then end with 0es up front
        trailing_padding = signature_binary[:-256]
        if binaryIsEmpty(trailing_padding, 0x00):
            assert securityPatchLevel == 0x00, "expected signature length indicator doesn't match the detected length"
            return signature_binary[-256:]

    if length > 512:
        # guess 512 placed at then end with 0es up front
        trailing_padding = signature_binary[:-512]
        if binaryIsEmpty(trailing_padding, 0x00):
            return signature_binary[-512:]

    # Possibly a lot of 0xFF at the end.
    sigBin = signature_binary.strip(b'\xFF')

    if len(sigBin) == 256:
        return sigBin

    if len(sigBin) == 512:
        return sigBin

    # Suspect an appended entry
    cookieOffset = signature_binary.find(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00$PS1')

    breakpoint()
    raise ValueError("Ehm what is going on here?")      # TODO better error message? More info?


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

        BODY_DATA_END = header.getSize() + header.getSignedSize()

        if header.isFirmwareCompressed():
            BODY_DATA_END = header.getSize() + header.getCompressedImageSize()

        assert BODY_DATA_END < TOTAL_SIZE, "More signed data then actual bytes in firmware"
        SIGNED_BODY = binary[header.getSize():BODY_DATA_END]

        ALIGNED_SIGNATURE_START = BODY_DATA_END
        if binary[BODY_DATA_END] == 0x00:
            ALIGNED_SIGNATURE_START = alignOffset(BODY_DATA_END, 16)

            assert ALIGNED_SIGNATURE_START < TOTAL_SIZE, f"Signature Start at {ALIGNED_SIGNATURE_START} exceeding total size of binary {TOTAL_SIZE}"

            padding_binary = binary[BODY_DATA_END:ALIGNED_SIGNATURE_START]
            assert binaryIsEmpty(padding_binary, 0x00), "Padding is not empty {padding_binary}"

        # trailing_binary = binary[ALIGNED_SIGNATURE_START:]
        # signature_binary = getSignatureFromTrailingBinary(trailing_binary, header.getSecurityPatchLevel())
        signatureSize = {
            0x00: 0x100,
            0x02: 0x200,
        }.get(header.getSecurityPatchLevel())

        signature_binary = bytes()
        trailing_binary = bytes()

        if signatureSize is not None:
            ALIGNED_SIGNATURE_END = ALIGNED_SIGNATURE_START + signatureSize
            signature_binary = binary[ALIGNED_SIGNATURE_START:ALIGNED_SIGNATURE_END]

            assert len(signature_binary) in [256, 512], "Signature of unexpected size"

            trailing_binary = binary[ALIGNED_SIGNATURE_END:]


            # testing things from the psp tool

            import struct
            p_signature_type = struct.unpack('<I', binary[0x34:0x38])[0]
            p_rom_size = struct.unpack('<I', binary[0x6c:0x70])[0]
            p_sig_offset = p_rom_size - signatureSize
            p_signature = binary[p_sig_offset:p_sig_offset + signatureSize]

            if p_signature != signature_binary:
                pass


        return cls(binary, offset, TOTAL_SIZE, firmwareType, header, SIGNED_BODY, signature_binary, trailing_binary)

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
                SIGNED_BINARY += zlib.decompress(self._signed_body)
            except:
                logging.error("Zlib decompression Failed")
                return False
        else:
            SIGNED_BINARY += self._signed_body

        valid = key.verify(self._signature_binary, SIGNED_BINARY)
        return valid

    def __init__(self, binary, offset: int, total_size: int, firmwareType: FirmwareType, header: PspFirmwareHeader, signed_body: bytes, signature_binary: bytes, trailing_binary: bytes):
        super().__init__()
        self._binary = binary
        assert firmwareType is not None, "firmwareType can't be None"
        self._offset = offset
        self._size = total_size
        self._firmwareType = firmwareType

        self._header: PspFirmwareHeader = header
        self._signed_body: bytes = signed_body
        self._signature_binary: bytes = signature_binary

        self._trailing_binary: bytes = trailing_binary

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
            "data": self._signed_body,
            "signature": self._signature_binary
        }

    def serialize(self) -> bytes:
        outputBinary = self._header.serialize()
        outputBinary += self._signed_body

        length = len(outputBinary)
        ALIGNED_LENGTH = alignOffset(length, 16)

        outputBinary = fillBinaryTill(outputBinary, ALIGNED_LENGTH, b'\x00')

        outputBinary += self._signature_binary

        if len(outputBinary) == self._size:
            return outputBinary

        outputBinary = fillBinaryTill(outputBinary, self._size)

        assert diffBinary(outputBinary, self._binary), "binary missmatch to unmodified copy"

        return outputBinary
