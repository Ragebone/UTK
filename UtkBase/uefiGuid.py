import struct


from UtkBase.interfaces.serializable import serializable


class UefiGuid(serializable):
    """
    UEFI GUID implementation
    """

    @classmethod
    def _struct(cls):
        return struct.Struct("<I H H 8s")

    @classmethod
    def fromBinary(cls, binary: bytes) -> 'UefiGuid':
        assert len(binary) == 16, "UefiGuid needs 16 bytes, got {}".format(len(binary))
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
        return 16

    def getName(self) -> str:
        from UtkBase import GuidDatabase
        """
        Retrieves a possible name for this GUID from the GUID Database.
        :return: Possible name for this GUID, default is "" to not clutter up output.
        """
        return GuidDatabase.getNameFromGuidString(self.guidString_read_only, "")

    def toString(self) -> str:
        """Return: Read Only string of the GUID"""
        return self.guidString_read_only

    def serialize(self) -> bytes:
        return self._struct().pack(self._data1, self._data2, self._data3, self._data4)
