from typing import Any

from UtkBase.images.volumes.files.sections.section import Section
from UtkBase.images.volumes.files.sections.sectionHeader import SectionHeader
from UtkBase.images.volumes.volume import Volume


class VolumeImageSection(Section):
    """
    A section that contains a UEFI Volume.

    """
    @classmethod
    def process(cls, binary: bytes, header: SectionHeader, sectionOffset: int = 0) -> 'VolumeImageSection':
        """
        Closed door / open door
        continued construction from  fromBinary() inheriting from Section

        this implements the parsing the UEFI Volume that those sections contain

        :param binary:
        :param header:
        :param sectionOffset: Optional informational offset
        :return:
        """
        HEADER_SIZE = header.getSize()
        binaryWithoutHeader = binary[HEADER_SIZE:]

        from UtkBase.images.volumes.volumeFactory import VolumeFactory

        offset = 0x00  # Bogus, because decompressed and start of section.
        uefiVolume = VolumeFactory.fromBinary(binaryWithoutHeader, offset)

        return cls(binaryWithoutHeader, header, uefiVolume, sectionOffset)

    def __init__(self, binary: bytes, header: SectionHeader, uefiVolume: Volume, sectionOffset: int = 0):
        super().__init__(binary, header, sectionOffset)

        assert uefiVolume is not None, "{} must be constructed with an UEFI Volume".format(self.__class__.__name__)
        self._volume = uefiVolume

    def getSize(self) -> int:
        # TODO make sure the size here is the correct size
        # Like the uncompressed and not the compressed or something
        return self._header.getSectionSize()

    def toDict(self) -> dict[str, Any]:
        return {
            "class": self.__class__.__name__,
            "sectionHeader": self._header,
            "volume": self._volume
        }

    def toString(self) -> str:
        outputString = self._header.toString()
        outputString += self._volume.toString()
        return outputString

    def serialize(self) -> bytes:
        outputBinary = self._header.serialize()
        outputBinary += self._volume.serialize()
        return outputBinary
