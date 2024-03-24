import traceback

from UtkBase.images.volumes.files.sections.byGuid.guidSectionFactory import GuidDefinedSectionFactory
from UtkBase.images.volumes.files.sections.section import Section
from UtkBase.images.volumes.files.sections.sectionHeaderFactory import SectionHeaderFactory
from UtkBase.images.volumes.files.sections.type import SectionType
from UtkBase.images.volumes.files.sections.volumeImageSection import VolumeImageSection


class SectionFactory:

    @staticmethod
    def fromBinary(binary: bytes, sectionOffset: int = 0) -> Section:
        sectionHeader = SectionHeaderFactory.fromBinary(binary)

        SECTION_TYPE: SectionType = sectionHeader.getSectionType()
        SECTION_SIZE = sectionHeader.getSectionSize()

        # limit binary
        binary = binary[:SECTION_SIZE]

        if SECTION_TYPE == SectionType.GuidDefined:
            try:
                guidDefinedSection = GuidDefinedSectionFactory.fromBinary(binary)
                return guidDefinedSection
            except Exception as ex:
                traceback.print_exception(type(ex), ex, ex.__traceback__)
                print("Falling back to generic Section")

        sectionClass = Section
        if SECTION_TYPE == SectionType.FirmwareVolumeImage:
            sectionClass = VolumeImageSection

        # TODO specific section implementations that allow for more capability
        section = sectionClass.fromBinary(binary, sectionHeader, sectionOffset)
        return section
