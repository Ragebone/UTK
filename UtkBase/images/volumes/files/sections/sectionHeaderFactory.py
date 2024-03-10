from UtkBase.images.volumes.files.sections.extendedSectionHeader import ExtendedSectionHeader
from UtkBase.images.volumes.files.sections.sectionHeader import SectionHeader


class SectionHeaderFactory:

    @staticmethod
    def fromBinary(binary: bytes):
        # TODO make nicer !
        try:
            sectionHeader = ExtendedSectionHeader.fromBinary(binary)
        except:
            sectionHeader = SectionHeader.fromBinary(binary)

        return sectionHeader
