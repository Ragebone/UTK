import logging

from UtkBase.images.volumes.files.file import File
from UtkBase.images.volumes.files.fileHeader import FileHeader
from UtkBase.images.volumes.files.sections.section import Section
from UtkBase.images.volumes.files.sections.sectionFactory import SectionFactory
from UtkBase.uefiGuid import UefiGuid
from UtkBase.utility import alignOffset, fillBinaryTill


# To what byte-count to align sections to.
# The default seems to be 4, it could vary though
SECTION_ALIGNMENT = 4

# The different possible padding values between sections.
# Sections seem to be padded with 0s instead of 0xFF as are UEFI volumes and most other things
SECTION_PADDINGS = [b'\x00\x00\x00', b'\x00\x00', b'\x00']


class SectionedFile(File):
    """
    A file containing sections.

    TODO add references to other implementations.
    """

    @classmethod
    def fromBinary(cls, binary: bytes, header=None, fileOffset: int = 0) -> 'SectionedFile':
        if header is None:
            header = FileHeader.fromBinary(binary)

        HEADER_SIZE = header.getSize()
        FILE_SIZE = header.getFileSize()

        # Self limit
        binary = binary[:FILE_SIZE]

        sections = {}

        offset = HEADER_SIZE
        while offset < FILE_SIZE:
            sectionBinary = binary[offset:]
            section: Section = SectionFactory.fromBinary(sectionBinary, offset)
            sections[hex(offset)] = section

            SECTION_SIZE = section.getSize()
            SECTION_END = offset + SECTION_SIZE
            ALIGNED_OFFSET = alignOffset(SECTION_END, SECTION_ALIGNMENT)

            paddingBinary = binary[SECTION_END:ALIGNED_OFFSET]

            if len(paddingBinary) > 0:
                if paddingBinary not in SECTION_PADDINGS:
                    logging.error("Padding between sections is not empty, discarding: {}".format(paddingBinary.hex().upper()))

            offset = ALIGNED_OFFSET

        # Add closedDoor / openDoor processing functionality
        arguments = cls.process(header, binary, sections, fileOffset)
        file = cls(*arguments)
        return file

    @classmethod
    def process(cls, header: FileHeader, binary: bytes, sections: dict[str, Section], fileOffset: int = 0) -> tuple:
        """
        ClosedDoor / openDoor processing functionality
        Allows subclasses to implement checking and handling differences specific to them
        Also allows for sharing the parsing of sections without redundancies

        :param header:
        :param binary:
        :param sections:
        :param fileOffset:
        :return:
        """
        return header, binary, sections, fileOffset

    def __init__(self, header: FileHeader, binary: bytes, sections=None, fileOffset: int = 0):
        super().__init__(header, binary, fileOffset)
        self._sections = {} if sections is None else sections

    def getSize(self) -> int:
        return self._header.getFileSize()

    def getGuid(self) -> UefiGuid:
        return self._header.getGuid()

    def getSortedSectionOffsets(self) -> list:
        return sorted(self._sections, key=lambda key: int(key, 16))

    def getSortedSections(self) -> list[tuple[str, Section]]:
        return sorted(self._sections.items(), key=lambda item: int(item[0], 16))

    def toDict(self) -> dict[str, any]:
        return {
            "offset": self._offset,
            "header": self._header,
            "sections": self._sections
        }

    def toString(self) -> str:
        return "Sectioned Uefi File"

    def serialize(self) -> bytes:
        outputBinary = self._header.serialize()

        sortedSections = self.getSortedSectionOffsets()
        for key in sortedSections:
            currentOffset = len(outputBinary)
            sectionOffset = int(key, 16)
            section = self._sections.get(key)

            assert currentOffset <= sectionOffset, "Section content overflow for offset {} with sectionOffset {}".format(
                hex(currentOffset), hex(sectionOffset)
            )

            # Paddings between sections
            outputBinary = fillBinaryTill(outputBinary, sectionOffset, b'\x00')

            sectionBinary = section.serialize()
            EXPECTED_SECTION_SIZE = section.getSize()
            BINARY_SIZE = len(sectionBinary)
            assert BINARY_SIZE == EXPECTED_SECTION_SIZE, "Section size missmatch for offset {} with size {}, expected {}".format(
                hex(sectionOffset), hex(BINARY_SIZE), hex(EXPECTED_SECTION_SIZE)
            )
            outputBinary += sectionBinary

        return outputBinary
