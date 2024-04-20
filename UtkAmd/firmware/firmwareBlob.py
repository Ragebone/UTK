from typing import Any

from UtkAmd.utkAmdInterfaces import AMD
from UtkBase.images.imageElement import ImageElement
from utkInterfaces import Header


class FirmwareBlob(ImageElement, AMD):
    """
    Generic class for handling all AMD Zen specific firmware.
    This is just meant to be a generic implementation to do nothing further with the firmware.
    """

    @classmethod
    def fromBinary(cls, binary: bytes, header: Header = None, offset: int = 0, firmwareType: int = 0xFF) -> 'ImageElement':
        """
        Construct a FirmwareBlob from the given binary
        The given binary has to contain everything including the header.
        Given Header objects will be ignored at this point

        NOTE the firmwareType is an unusual addition to the function.
        Firmware Type corresponds to the "Type" number defined by AMD.
        """
        return cls(offset, binary, firmwareType)

    def __init__(self, offset: int, binary: bytes, firmwareType: int = 0xFF):
        self._offset = offset
        self._firmwareType = firmwareType
        self._binary: bytes = binary
        self._size = len(binary)

    def getSize(self) -> int:
        return self._size

    def getOffset(self) -> int:
        return self._offset

    def toDict(self) -> dict[str, Any]:
        return {
            "offset": self._offset,
            "type": self._firmwareType,
            "size": self._size,
            "binary": self._binary
        }

    def serialize(self) -> bytes:
        return self._binary
