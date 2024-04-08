import struct
from typing import Any

from utkInterfaces import Serializable


class UefiGuid(Serializable):
    """
    UEFI GUID implementation.
    A 128-Bit, 16-Byte unsigned integer.
    Commonly written as multiple smaller numbers;

    32-Bit, unsigned integer
    2x 16-bit unsigned integer
    8 Byte individual bytes
    Random numbers for example:
    {0xDEADBEEF, 0x1234, 0x5678,  {0x12, 0x34, 0x56, 0x78, 0x9A, 0xBC, 0xDE 0xFF}}
    Beware that this representation does not easily match the string-representation like:
    TODO execute the below thing and add the string representation here.
    myUefiGuid = UefiGuid(0xDEADBEEF, 0x1234, 0x5678, b'\x12\x34\x56\x78\x9A\xBC\xDE\xFF')
    """

    @classmethod
    def _struct(cls):
        return struct.Struct("<I H H 8s")

    @classmethod
    def fromBinary(cls, binary: bytes) -> 'UefiGuid':
        assert len(binary) == 16, "UefiGuid needs 16 bytes, got {}; {}".format(len(binary), binary.hex().upper())
        return cls(*cls._struct().unpack(binary))

    def __init__(self, data1: int, data2: int, data3: int, data4: bytes):
        self._data1: int = data1
        self._data2: int = data2
        self._data3: int = data3
        self._data4: bytes = data4

        # Read-Only string representation so that debugging is easier
        self.guidString_read_only = "{:08X}-{:04X}-{:04X}-{:02X}{:02X}-{:02X}{:02X}{:02X}{:02X}{:02X}{:02X}".format(
            data1, data2, data3, *data4
        )

    def getSize(self) -> int:
        """Size of the UEFI GUID; 16 bytes, 128-Bits"""
        return 16

    def getName(self, whenUnknown: Any = "") -> str:
        from UtkBase import GuidDatabase
        """
        Retrieves a possible name for this GUID from the GUID Database.
        :return: Possible name for this GUID, default is "" to not clutter up output.
        """
        return GuidDatabase.getNameFromGuidString(self.guidString_read_only, whenUnknown)

    def toDict(self) -> dict[str, Any]:
        name = self.getName(None)
        if name is None:
            return {
                "guidString": self.guidString_read_only,
                "guidName": name
            }
        return {"guidString": self.guidString_read_only}

    def toString(self) -> str:
        """Return: Read Only string of the GUID"""
        return self.guidString_read_only

    def serialize(self) -> bytes:
        """ Serializable """
        return self._struct().pack(self._data1, self._data2, self._data3, self._data4)
