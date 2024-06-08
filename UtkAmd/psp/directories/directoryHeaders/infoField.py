from ctypes import LittleEndianStructure,  c_uint32
from typing import Any

from UtkAmd.psp.addressMode import AddressMode
from UtkAmd.utkAmdInterfaces import UtkAMD
from utkInterfaces import Serializable


class PspDirectoryHeaderInfoField(LittleEndianStructure, Serializable, UtkAMD):
    """
    Info filed part of PSP Directory Headers

    Source:
    https://github.com/openSIL/AGCL-R/blob/6a414aff86de63e5c2a6dfec05b8560291b04e0b/AgesaPkg/Include/AmdPspDirectory.h#L35
    """

    _fields_ = [
        ("_maxSize", c_uint32, 10),
        ("_spiBlockSize", c_uint32, 4),
        ("_baseAddress", c_uint32, 15),
        ("_addressModeValue", c_uint32, 2),
        ("_reserved", c_uint32, 1),
    ]

    @classmethod
    def fromBinary(cls, binary: bytes) -> 'PspDirectoryHeaderInfoField':
        infoFiled = cls.from_buffer_copy(binary)
        addressModeValue = infoFiled._addressModeValue

        # Enum is supposed to supersede the int in the structure
        infoFiled._addressMode = AddressMode(addressModeValue)
        return infoFiled

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        # NOTE this will not be executed when calling "fromBinary()"
        super().__init__(*args, **kwargs)
        self._addressMode: AddressMode

    def getAddressMode(self) -> AddressMode:
        return self._addressMode

    def getMaxSize(self) -> int:
        return self._maxSize

    def getSpiBlockSize(self) -> int:
        return self._spiBlockSize

    def toDict(self) -> dict[str, Any]:
        return {
            "maxSize": self._maxSize,
            "spiBlockSize": self._spiBlockSize,
            "baseAddress": self._baseAddress,
            "addressMode": self._addressMode,
            "reserved": self._reserved,
        }

    def serialize(self) -> bytes:
        # Override the structure value with the actual enum objects value
        self._addressModeValue = self._addressMode.value
        return bytes(self)
