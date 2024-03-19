import struct
from typing import Any

from UtkBase.images.volumes.files.sections.type import SectionType
from UtkBase.interfaces.serializable import serializable, serializeAsJsonFile


class SectionHeader(serializable, serializeAsJsonFile):
    """
    # TODO Add version 2 headers:
    # https://github.com/LongSoft/UEFITool/blob/bf93a5eacc900de3b2665f0bbe52d116aa1fba25/common/ffsparser.cpp#L2297
    # https://github.com/Kostr/UEFI-Lessons/blob/master/Lessons_uncategorized/Lesson_FDF_FV_2/README.md
    """

    @classmethod
    def _struct(cls):
        return struct.Struct('3s B')

    @classmethod
    def fromBinary(cls, binary: bytes) -> 'SectionHeader':
        return cls(*cls._struct().unpack(binary[:cls._struct().size]))

    def __init__(self, sectionSizeBinary: bytes, sectionType: int):
        assert isinstance(sectionSizeBinary, bytes), "SectionSize must be 3 bytes as a 24 Bit uint"
        assert len(sectionSizeBinary) == 3, "SectionSize not 3 bytes"
        sectionSize, = struct.unpack('<I', sectionSizeBinary + b'\x00')

        self._sectionSize = sectionSize
        self._sectionType: SectionType = SectionType(sectionType)

    def getSize(self) -> int:
        return self._struct().size

    def getSectionSize(self) -> int:
        return self._sectionSize

    def getSectionType(self) -> SectionType:
        return self._sectionType

    def toDict(self) -> dict[str, Any]:
        return {
            "class": self.__class__.__name__,
            "sectionSize": self._sectionSize,
            "sectionType": self._sectionType
        }

    def toString(self) -> str:
        return "Section Size: {}, Type: {}\n".format(hex(self._sectionSize), hex(self._sectionType.value))

    def serialize(self) -> bytes:
        size24 = struct.pack('<I', self._sectionSize)[:3]
        return self._struct().pack(size24, self._sectionType.value)
