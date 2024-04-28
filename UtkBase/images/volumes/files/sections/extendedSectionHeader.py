import struct

from UtkBase.images.volumes.files.sections.sectionHeader import SectionHeader


class ExtendedSectionHeader(SectionHeader):
    """
    # https://github.com/tianocore/edk2/blob/beafabdae49c873adecdb7511dbebe9d4ff5c8f0/MdePkg/Include/Pi/PiFirmwareFile.h#L252C30-L252C30
    """
    @classmethod
    def _struct(cls):
        return struct.Struct('3s B I')

    # inherited fromBinary from SectionHeader
    # TODO this could be nicer!

    def __init__(self, sectionSizeBinary: bytes, sectionType: int, extendedSize: int):
        assert sectionSizeBinary == b'\xFF\xFF\xFF', "Not an Extended Section Header, size must be 0xFFFFFF, got {}".format(sectionSizeBinary.hex().upper())
        super().__init__(sectionSizeBinary, sectionType)
        self._extendedSize = extendedSize

    def getSectionSize(self):
        return self._extendedSize

    def toDict(self) -> dict[str, any]:
        return {
            "sectionSize": self._sectionSize,
            "sectionType": self._sectionType
        }

    # TODO proper toString
    def toString(self):
        return "Extended Section Header\n"

    def serialize(self) -> bytes:
        size24 = struct.pack('<I', self._sectionSize)[:3]
        return self._struct().pack(size24, self._sectionType.value, self._extendedSize)
