import struct

from UtkBase.interfaces.serializable import serializable


class UefiGuid(serializable):

    @classmethod
    def _struct(cls):
        return struct.Struct("<I H H 8s")

    @classmethod
    def fromBinary(cls, binary: bytes, **kwargs):
        assert len(binary) == 16, "UefiGuid needs 16 bytes, got {}".format(len(binary))
        return cls(*cls._struct().unpack(binary))

    def __init__(self, data1: int, data2: int, data3: int, data4: bytes):
        self._data1: int = data1
        self._data2: int = data2
        self._data3: int = data3
        self._data4: bytes = data4
        self.guidString_RO = self.toString()

    def getSize(self):
        return 16

    def toString(self):
        return "{:08X}-{:04X}-{:04X}-{:02X}{:02X}-{:02X}{:02X}{:02X}{:02X}{:02X}{:02X}".format(self._data1, self._data2, self._data3, *self._data4)

    def serialize(self):
        return self._struct().pack(self._data1, self._data2, self._data3, self._data4)
