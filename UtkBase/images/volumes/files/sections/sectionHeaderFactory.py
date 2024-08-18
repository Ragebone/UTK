from UtkBase.images.volumes.files.sections.extendedSectionHeader import ExtendedSectionHeader
from UtkBase.images.volumes.files.sections.sectionHeader import SectionHeader


class SectionHeaderFactory:

    @staticmethod
    def fromBinary(binary: bytes):
        # TODO make nicer !

        sectionSizeBinary = binary[:3]
        if sectionSizeBinary == b'\xFF\xFF\xFF':
            return ExtendedSectionHeader.fromBinary(binary)

        return SectionHeader.fromBinary(binary)

