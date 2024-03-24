from UtkBase.images.volumes.files.sections.byGuid.headerExtension import HeaderExtension
from UtkBase.images.volumes.files.sections.byGuid.lzmaCompressed import LzmaCompressedSection
from UtkBase.images.volumes.files.sections.section import Section
from UtkBase.images.volumes.files.sections.sectionHeader import SectionHeader
from UtkBase.images.volumes.files.sections.sectionHeaderFactory import SectionHeaderFactory

# TODO other Sections and verification that those sections here work correctly
_guidDefinedSectionMapping = {
    "FC1BCDB0-7D31-49AA-936A-A4600D9DD083": None,                       # EFI_GUIDED_SECTION_CRC32
    "A31280AD-481E-41B6-95E8-127F4C984779": None,                       # EFI_GUIDED_SECTION_TIANO

    "EE4E5898-3914-4259-9D6E-DC7BD79403CF": LzmaCompressedSection,      # EFI_GUIDED_SECTION_LZMA
    "0ED85E23-F253-413F-A03C-901987B04397": LzmaCompressedSection,      # EFI_GUIDED_SECTION_LZMA_HP
    "D42AE6BD-1352-4BFB-909A-CA72A6EAE889": LzmaCompressedSection,      # EFI_GUIDED_SECTION_LZMAF86
    "1D301FE9-BE79-4353-91C2-D23BC959AE0C": None,                       # EFI_GUIDED_SECTION_GZIP
    "CE3233F5-2CD6-4D87-9152-4A238BB6D1C4": LzmaCompressedSection,      # EFI_GUIDED_SECTION_ZLIB_AMD
    "991EFAC0-E260-416B-A4B8-3B153072B804": LzmaCompressedSection,      # EFI_GUIDED_SECTION_ZLIB_AMD2
    "0F9D89E8-9259-4F76-A5AF-0C89E34023DF": None                        # EFI_FIRMWARE_CONTENTS_SIGNED_GUID
}


class GuidDefinedSectionFactory:

    @staticmethod
    def fromBinary(binary: bytes, sectionHeader: SectionHeader = None, sectionOffset: int = 0) -> Section:

        if sectionHeader is None:
            sectionHeader: SectionHeader = SectionHeaderFactory.fromBinary(binary)

        HEADER_SIZE = sectionHeader.getSize()
        headerExtension = HeaderExtension.fromBinary(binary[HEADER_SIZE:])

        sectionGuid = headerExtension.getGuidString()
        guidedSectionClass = _guidDefinedSectionMapping.get(sectionGuid, None)
        assert guidedSectionClass is not None, "Section defined by GUID with GUID {} is still unknown and not implemented".format(sectionGuid)

        # TODO  well,  the HeaderExtension should be passed onwards, otherwise it is wasted here and has to be rebuild. Not bad welp.
        section = guidedSectionClass.fromBinary(binary, sectionHeader, sectionOffset, headerExtension)
        return section
