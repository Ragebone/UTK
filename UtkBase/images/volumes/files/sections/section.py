from typing import Any

from UtkBase.images.volumes.files.sections.sectionHeader import SectionHeader
from UtkBase.images.volumes.files.sections.sectionHeaderFactory import SectionHeaderFactory
from UtkBase.interfaces.serializable import serializable


class Section(serializable):
    @classmethod
    def fromBinary(cls, binary: bytes, header: SectionHeader = None) -> 'Section':
        if header is None:
            header = SectionHeaderFactory.fromBinary(binary)

        SECTION_SIZE = header.getSectionSize()
        binary = binary[:SECTION_SIZE]
        BINARY_SIZE = len(binary)
        assert BINARY_SIZE == SECTION_SIZE, "{} has a differing amount of bytes. Expected: {} Got: {}".format(cls.__name__, hex(SECTION_SIZE), hex(BINARY_SIZE))

        # Closed door / open door
        section = cls.process(binary, header)
        return section

    @classmethod
    def process(cls, binary: bytes, header: SectionHeader) -> 'Section':
        HEADER_SIZE = header.getSize()
        binaryWithoutHeader = binary[HEADER_SIZE:]

        return cls(binaryWithoutHeader, header)

    def __init__(self, binary: bytes, header: SectionHeader):
        self._binary = binary
        self._header = header

    def getSize(self) -> int:
        return self._header.getSectionSize()

    def toDict(self) -> dict[str, Any]:
        return {
            "class": self.__class__.__name__,
            "sectionHeader": self._header,
            "binary": self._binary
        }

    def toString(self) -> str:
        return "{}      {}\n".format(self._header.toString(), self.__class__.__name__)

    def serialize(self) -> bytes:
        outputBinary = self._header.serialize()
        outputBinary += self._binary
        return outputBinary

