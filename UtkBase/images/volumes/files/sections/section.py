from UtkBase.images.volumes.files.sections.sectionHeader import SectionHeader
from UtkBase.images.volumes.files.sections.sectionHeaderFactory import SectionHeaderFactory
from utkInterfaces import Serializable


class Section(Serializable):
    @classmethod
    def fromBinary(cls, binary: bytes, header: SectionHeader = None, sectionOffset: int = 0, *kwargs) -> 'Section':
        """
        Construct a Section* from the given binary.
        This is function is pretty Generic and does not distinguish anything.

        It can be any type of Section with "cls.process(...)" handling the Class specific parsing

        :param binary: Bytes to build the Section from
        :param header: Optional previously constructed SectionHeader
        :param sectionOffset: Optional informational offset where the section is within the File
        :param kwargs: Additional unspecified keyword arguments to pass to the process function
        Arguments for the specific Section implementation it is going to be.
        Probably a GUID Defined Section with a HeaderExtension
        :return: The built Section
        """
        if header is None:
            header = SectionHeaderFactory.fromBinary(binary)

        SECTION_SIZE = header.getSectionSize()
        binary = binary[:SECTION_SIZE]
        BINARY_SIZE = len(binary)
        assert BINARY_SIZE == SECTION_SIZE, "{} has a differing amount of bytes. Expected: {} Got: {}".format(cls.__name__, hex(SECTION_SIZE), hex(BINARY_SIZE))

        # Closed door / open door
        section = cls.process(binary, header, sectionOffset, *kwargs)
        return section

    @classmethod
    def process(cls, binary: bytes, header: SectionHeader, sectionOffset: int = 0, *kwargs) -> 'Section':
        HEADER_SIZE = header.getSize()
        binaryWithoutHeader = binary[HEADER_SIZE:]

        return cls(binaryWithoutHeader, header, sectionOffset)

    def __init__(self, binary: bytes, header: SectionHeader, sectionOffset: int = 0):
        self._offset = sectionOffset
        self._binary = binary
        self._header = header

    def getSize(self) -> int:
        return self._header.getSectionSize()

    def toDict(self) -> dict[str, any]:
        return {
            "offset": self._offset,
            "sectionHeader": self._header,
            "binary": self._binary
        }

    def toString(self) -> str:
        return "{}      {}\n".format(self._header.toString(), self.__class__.__name__)

    def serialize(self) -> bytes:
        outputBinary = self._header.serialize()
        outputBinary += self._binary
        return outputBinary

