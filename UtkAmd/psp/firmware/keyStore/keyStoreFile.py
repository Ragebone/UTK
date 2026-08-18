from UtkAmd.psp.firmware.firmwareHeaders.firmwareHeaderFactory import FirmwareHeaderFactory
from UtkAmd.psp.firmware.firmwareHeaders.pspFirmwareHeader import PspFirmwareHeader
from UtkAmd.psp.firmware.keyStore.store import KeyStore
from UtkAmd.psp.firmware.signedFirmwareBlob import SignedFirmwareBlob
from UtkAmd.psp.firmwareTypes import FirmwareType
from UtkCommon.interfaces.reference import Reference


class KeyStoreFile(SignedFirmwareBlob):
    """
    TODO it could be that the Header structure for this is different from the usual headers.
    Magic still seems to be $PS1 though

    """
    def getParent(self) -> any:
        pass

    def setParent(self, parent: 'Image') -> None:
        pass

    @classmethod
    def continue_with_body(cls, binary, offset: int, total_size: int, firmwareType: FirmwareType, header: PspFirmwareHeader, body: bytes, signature_binary: bytes):
        keyStoreage = KeyStore.fromBinary(body)
        return cls(binary, offset, total_size, firmwareType, header, keyStoreage, signature_binary)

    def __init__(self, binary, offset: int, total_size: int, firmwareType: FirmwareType, header: PspFirmwareHeader, keyStoreage, signature_binary: bytes):
        self._binary = binary
        assert firmwareType is not None, "firmwareType can't be None"
        self._offset = offset
        self._size = total_size
        self._firmwareType = firmwareType

        self._header: PspFirmwareHeader = header
        self._keyStore = keyStoreage
        self._signature_binary: bytes = signature_binary

        self._references: list[Reference] = []

    def serialize(self) -> bytes:
        return self._binary
