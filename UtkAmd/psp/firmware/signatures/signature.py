from UtkAmd.psp.firmware.firmwareBlob import FirmwareBlob
from UtkAmd.psp.firmwareTypes import FirmwareType
from utkInterfaces import Header


class Signature(FirmwareBlob):
    """

    """
    @classmethod
    def fromBinary(cls, binary: bytes, header: Header = None, offset: int = 0, firmwareType: FirmwareType = None) -> 'Signature':
        assert header is None, "Signatures can't have a header"
        return cls(binary, offset, firmwareType)

    def __init__(self, binary: bytes, offset: int, firmwareType: FirmwareType):
        super().__init__(offset, binary, firmwareType)

    def getSize(self) -> int:
        return len(self._binary)

    def toDict(self) -> dict[str, any]:
        return {
            "offset": self._offset,
            "type": self._firmwareType,
            "size": self._size,
            "binary": self._binary
        }

    def serialize(self) -> bytes:
        return self._binary
