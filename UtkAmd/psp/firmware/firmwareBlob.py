from UtkAmd.psp.firmware.firmwareInterface import Firmware
from UtkAmd.psp.firmwareTypes import FirmwareType
from UtkAmd.utkAmdInterfaces import UtkAMD
from UtkBase import utility
from utkInterfaces import Header, Reference


class FirmwareBlob(Firmware, UtkAMD):
    """
    Generic class for handling all AMD Zen specific firmware.
    This is just meant to be a generic implementation to do nothing further with the firmware.
    """

    @classmethod
    def fromBinary(cls, binary: bytes, header: Header = None, offset: int = 0, firmwareType: FirmwareType = None) -> 'Firmware':
        """
        Construct a FirmwareBlob from the given binary
        The given binary has to contain everything including the header.
        Given Header objects will be ignored at this point

        NOTE the firmwareType is an unusual addition to the function.
        Firmware Type corresponds to the "Type" number defined by AMD.
        """
        #if header is not None:
            #binary = binary[header.getSize():]
            # TODO Limiting the binary here has some risks, Figure out where to do that better
        return cls(offset, binary, firmwareType, header)

    def __init__(self, offset: int, binary: bytes, firmwareType: FirmwareType, header: Header = None):
        assert firmwareType is not None, "firmwareType can't be None"
        self._offset = offset
        self._firmwareType = firmwareType
        self._binary: bytes = binary
        self._size = len(binary)
        self._header: Header = header

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
            "type": self._firmwareType,
            "size": self._size,
            "header": self._header,
            "binary": self._binary
        }

    def serialize(self) -> bytes:

        if self._header is not None:
            outputBinary = bytes()
            outputBinary += self._header.serialize()

            outputBinary += self._binary[0x100:]

            return outputBinary

        return self._binary
