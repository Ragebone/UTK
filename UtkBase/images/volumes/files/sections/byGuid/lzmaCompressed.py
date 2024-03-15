import logging
import lzma

from lzma import LZMADecompressor, FORMAT_ALONE


from UtkBase.images.volumes.files.sections.byGuid.headerExtension import HeaderExtension
from UtkBase.images.volumes.files.sections.section import Section
from UtkBase.images.volumes.files.sections.sectionHeader import SectionHeader
from UtkBase.images.volumes.files.sections.sectionHeaderFactory import SectionHeaderFactory
from UtkBase.utility import alignOffset, fillBinaryTill

SECTION_ALIGNMENT = 4


class LzmaCompressedSection(Section):

    @classmethod
    def process(cls, binary: bytes, header: SectionHeader, headerExtension=None) -> 'Section':
        """
             Create a GuidedLzma from the given binary
             :param binary: Full binary including all headers and extensions
             :param header:
             :param headerExtension:
             :return:
         """
        if header is None:
            header = SectionHeaderFactory.fromBinary(binary)

        HEADER_SIZE = header.getSize()
        binaryWithoutHeader = binary[HEADER_SIZE:]

        if headerExtension is None:
            headerExtension = HeaderExtension.fromBinary(binaryWithoutHeader)

        # Self limit
        binaryWithoutHeaders = binaryWithoutHeader[headerExtension.getSize():]

        lzmaDecompressor = LZMADecompressor(format=FORMAT_ALONE, memlimit=None, filters=None)
        decompressedBinary = lzmaDecompressor.decompress(binaryWithoutHeaders, -1)

        from UtkBase.images.volumes.files.sections.sectionFactory import SectionFactory

        DECOMPRESSED_SIZE = len(decompressedBinary)

        sections = {}

        # TODO move this to a better location so that it is not redundant with the SectionedFile
        offset = 0
        while offset < DECOMPRESSED_SIZE:
            sectionBinary = decompressedBinary[offset:]
            section = SectionFactory.fromBinary(sectionBinary)
            sections[hex(offset)] = section

            SECTION_SIZE = section.getSize()
            SECTION_END = offset + SECTION_SIZE
            ALIGNED_OFFSET = alignOffset(SECTION_END, SECTION_ALIGNMENT)

            paddingBinary = binary[SECTION_END:ALIGNED_OFFSET]

            if len(paddingBinary) > 0 and paddingBinary != b'\x00\x00':
                logging.error(
                    "Padding between sections is not empty, discarding: {}".format(paddingBinary.hex().upper()))

            offset = ALIGNED_OFFSET

        lzmaCompressedSection = cls(binaryWithoutHeaders, header, headerExtension, sections)
        return lzmaCompressedSection

    def __init__(self, binary: bytes, header: SectionHeader, headerExtension: HeaderExtension, sections: dict):
        super().__init__(binary, header)
        self._headerExtension = headerExtension
        self._sections = sections

    def getSize(self) -> int:
        return self._header.getSectionSize()

    def getSortedSectionOffsets(self) -> list:
        return sorted(self._sections, key=lambda key: int(key, 16))

    def toString(self) -> str:
        outputString = self._header.toString()
        for section in self._sections:
            outputString += section.toString()
        return outputString

    def serialize(self) -> bytes:
        # TODO Serialization of the actual sections and compression back.
        # Problem here are the weird compression settings that need to match, otherwise things are gona be not as expected.
        # Or the input won't equal the output.
        # That would still be bad here

        outputBinary = self._header.serialize()
        outputBinary += self._headerExtension.serialize()

        uncompressedBinary = bytes()
        sortedSections = self.getSortedSectionOffsets()
        for key in sortedSections:
            currentOffset = len(uncompressedBinary)
            sectionOffset = int(key, 16)
            section = self._sections.get(key)

            assert currentOffset <= sectionOffset, "Section content overflow for offset {} with sectionOffset {}".format(
                hex(currentOffset), hex(sectionOffset)
            )

            # Paddings between sections
            uncompressedBinary = fillBinaryTill(uncompressedBinary, sectionOffset, b'\x00')

            sectionBinary = section.serialize()
            EXPECTED_SECTION_SIZE = section.getSize()
            BINARY_SIZE = len(sectionBinary)
            assert BINARY_SIZE == EXPECTED_SECTION_SIZE, "Section size missmatch for offset {} with size {}, expected {}".format(
                hex(sectionOffset), hex(BINARY_SIZE), hex(EXPECTED_SECTION_SIZE)
            )
            uncompressedBinary += sectionBinary

        # supposedly, Level = 9, fb = 273.
        # The closest size to what it previously was, seems to be preset 5
        # TODO this breaks the serialization equals tests
        compresedBinary = lzma.compress(uncompressedBinary, format=FORMAT_ALONE, check=-1, preset=5, filters=None)

        outputBinary += compresedBinary

        return outputBinary
