from ctypes import c_uint8, c_bool, LittleEndianStructure

from UtkAmd.utkAmdInterfaces import UtkAMD
from utkInterfaces import Serializable


class BiosTypeAttribute(LittleEndianStructure, Serializable, UtkAMD):
    """
    Attribute field as is used in BiosDirectoryEntries

    Source for this extensive and specific structure in the OpenSIL AGCL-R:
    https://github.com/openSIL/AGCL-R/blob/c1789df006acab5e1ac1c52ec114c3de2230f54b/AgesaPkg/Include/AmdPspDirectory.h#L268
    """

    _fields_ = [
        # ("_typeValue", c_uint8, 8),           # Implemented seperately
        ("_reloadOnS3Resume", c_bool, 1),
        ("_reserved", c_uint8, 7),
        ("_isBiosResetImage", c_bool, 1),
        ("_copy", c_bool, 1),
        ("_isReadOnly", c_bool, 1),
        ("_isCompressed", c_bool, 1),
        ("_instance", c_uint8, 4),
        ("_subProgram", c_uint8, 3),
        ("_romId", c_uint8, 2),
        ("_isWritable", c_bool, 1),
        ("_reserved1", c_uint8, 2),
    ]

    @classmethod
    def fromBinary(cls, binary: bytes) -> 'BiosTypeAttribute':
        biosTypeAttribute = cls.from_buffer_copy(binary)
        return biosTypeAttribute

    def __init__(self, *args: any, **kw: any):
        """
        :param s3Reload: bool
        :param reserved1: uint8
        :param biosResetImage: bool
        :param copy: bool
        :param readOnly: bool
        :param compressed: bool
        :param instance: uint8
        :param subProgram: uint8
        :param romId: uint8
        :param writable: bool
        :param reserved: uint8
        """
        super().__init__(*args, **kw)

    def toDict(self) -> dict[str, any]:
        return {
            # "typeValue": self._typeValue,
            "reloadOnS3Resume": self._reloadOnS3Resume,
            "reserved": self._reserved,
            "biosResetImage": self._isBiosResetImage,
            "copy": self._copy,
            "isReadOnly": self._isReadOnly,
            "isCompressed": self._isCompressed,
            "instance": self._instance,
            "subProgram": self._subProgram,
            "RomId": self._romId,
            "isWritable": self._isWritable,
            "reserved1": self._reserved1,
        }

    def serialize(self) -> bytes:
        return bytes(self)
