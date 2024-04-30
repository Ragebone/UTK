import abc

from UtkAmd.psp.firmware.firmwareFactory import FirmwareFactory
from UtkAmd.psp.directories.directoryHeaders.pspDirectoryHeader import PspDirectoryHeader
from UtkAmd.psp.directories.directoryEntries.directoryEntry import DirectoryEntry, TypedDirectoryEntry
from UtkAmd.psp.directories.directoryHeaders.directoryHeader import DirectoryHeader
from UtkAmd.utkAmdInterfaces import UtkAMD
from UtkBase.images.imageElement import ImageElement
from UtkBase.utility import binaryIsEmpty, fillBinaryTill

# start of the directory content
CONTENT_OFFSET = 0x400


class Directory(ImageElement, UtkAMD):
    """
    Common interface for all directories, those being psp, bios and combo -directories
    Declares what a Directory in an AmdImage has to be capable of
    """

    @abc.abstractmethod
    def getDirectoryEntries(self):
        pass

    @abc.abstractmethod
    def getOffset(self):
        pass

    @abc.abstractmethod
    def getHeader(self):
        pass


class ContentDirectory(Directory):
    """
    Interface and partial implementation for psp and bios -directories that also act as a container.

    Such directories look as follows:
    - Header
    - [?] DirectoryEntries
        - trailing binary if there aren't just 0xFFs; only 0xFF -> None
    At 0x400 bytes:
    - [?] Directory Items

    If the location , offset or reference in the TypedDirectoryEntry points into another directory or into the image:
    Then the entry is to be classified as a PointDirectoryEntry.
    """

    @classmethod
    @abc.abstractmethod
    def _buildDirectoryEntry(cls, binary: bytes) -> DirectoryEntry:
        """
        Build the Bios or PSP -directory specific DirectoryEntry

        :param binary: Binary to build the DirectoryEntry from
        :return: The new DirectoryEntry
        """
        pass

    # TODO add a Validate function to the interface. Some place needs to check weather the header is the correct one etc.

    #
    # Implementation that is identical between Psp and Bios Directories
    #

    @classmethod
    def fromBinary(cls, binary: bytes, header: PspDirectoryHeader = None, directoryOffset: int = None, **kwargs) -> 'Directory':
        assert binary is not None, "Binary is None"

        if header is None:
            header: DirectoryHeader = PspDirectoryHeader.fromBinary(binary)

        assert header is not None, "PSP Directory Header is None and shouldn't be"

        DIRECTORY_SIZE = header.getDirectorySize()
        DIRECTORY_END = directoryOffset + DIRECTORY_SIZE

        directoryEntries, TRAILING_BINARY = cls.buildDirectoryEntries(binary, header, directoryOffset, DIRECTORY_END)

        directoryContent = {}

        for dirEntry in directoryEntries:
            if not isinstance(dirEntry, TypedDirectoryEntry):
                continue

            if dirEntry.isPointEntry():
                # Points to something outside the directories content area.
                # Needs to be handled on the AmdImage level
                continue

            entryOffset = dirEntry.getEntryLocation()

            # EXPECTATION  entryOffset is a flashOffset
            if directoryOffset <= entryOffset < directoryOffset + CONTENT_OFFSET:
                # invalid offset pointing somewhere into the non-content area of the directory.
                continue

            ENTRY_SIZE = dirEntry.getEntrySize()

            # relative to directory and its binary
            RELATIVE_ENTRY_START = entryOffset - directoryOffset
            RELATIVE_ENTRY_END = RELATIVE_ENTRY_START + ENTRY_SIZE

            ENTRY_BINARY = binary[RELATIVE_ENTRY_START:RELATIVE_ENTRY_END]
            ENTRY_BINARY_SIZE = len(ENTRY_BINARY)

            assert ENTRY_BINARY_SIZE == ENTRY_SIZE, f"Entry binary with size {hex(ENTRY_BINARY_SIZE)} does not match expected {hex(ENTRY_SIZE)}"

            firmware = FirmwareFactory.fromBinary(dirEntry.getEntryType(), ENTRY_BINARY, RELATIVE_ENTRY_START)
            directoryContent[hex(RELATIVE_ENTRY_START)] = firmware

        directory = cls(directoryOffset, header, directoryEntries, directoryContent, TRAILING_BINARY)
        return directory

    @classmethod
    def buildDirectoryEntries(cls, binary: bytes, header: DirectoryHeader, directoryStart: int, directoryEnd: int) -> tuple[list[DirectoryEntry], bytes]:
        """
        Builds / Parses the DirectoryEntries

        :param binary: Binary to parse from, starting at the first DirectoryEntry
        :param header: The Directories Header needed for the process
        :param directoryStart: Offset number where the directory starts, needed for PointEntry decision-making
        :param directoryEnd: Offset number where the directory ends, needed for PointEntry decision-making
        :return: tuple, list[DirectoryEntry], the trailing binary or None if it is just empty 0xFF bytes
        """
        directoryEntries = []

        STRUCTURE_BINARY = binary[header.getSize():CONTENT_OFFSET]

        offset = 0
        NUMBER_OF_DIR_ENTRIES = header.getEntryCount()
        for index in range(NUMBER_OF_DIR_ENTRIES):
            DIR_ENTRY_BINARY = STRUCTURE_BINARY[offset:]
            dirEntry: DirectoryEntry = cls._buildDirectoryEntry(DIR_ENTRY_BINARY)

            # TODO this is sooo bad,  this only works if it is an absolute offset that does not need to be masked
            if isinstance(dirEntry, TypedDirectoryEntry):
                entryOffset = dirEntry.getEntryLocation()
                if not (directoryStart <= entryOffset <= directoryEnd):
                    dirEntry.setAsPointEntry()

            directoryEntries.append(dirEntry)
            offset += dirEntry.getSize()

        TRAILING_BINARY = STRUCTURE_BINARY[offset:]
        if binaryIsEmpty(TRAILING_BINARY):
            # Don't need to store it
            TRAILING_BINARY = None

        return directoryEntries, TRAILING_BINARY

    def __init__(self, offset: int, header: PspDirectoryHeader, directoryEntries: list[DirectoryEntry], content: dict[str, any], trailingBinary: bytes = None):
        assert header is not None, "Header can't be None for Directory"

        self._offset: int = offset

        self._header = header

        self._directoryEntries: list[DirectoryEntry] = directoryEntries
        self._content: dict[str, ImageElement] = content
        self._trailingBinary: bytes = trailingBinary

    def getDirectoryEntries(self) -> list[DirectoryEntry]:
        """Get copied List of directoryEntries"""
        return self._directoryEntries.copy()

    def getHeader(self) -> PspDirectoryHeader:
        """Get Reference of DirectoryHeader"""
        return self._header

    def getSize(self) -> int:
        return self._header.getDirectorySize()

    def getOffset(self) -> int:
        return self._offset

    def getContent(self) -> list[tuple[str, ImageElement]]:
        """
        Get a copy of the directories content, as tuples with and sorted by its offset.

        :return: List  (offset as hex string), ImagElement
        """
        return sorted(self._content.items(), key=lambda item: int(item[0], 16))

    def toDict(self) -> dict[str, any]:
        return {
            "offset": self._offset,
            "directoryHeader": self._header,
            "directoryEntries": self._directoryEntries,
            "trailingBinary": self._trailingBinary,
            "content": self._content
        }

    def serialize(self) -> bytes:
        outputBinary = self.getHeader().serialize()

        for dirEntry in self.getDirectoryEntries():
            outputBinary += dirEntry.serialize()

        if self._trailingBinary is None:
            outputBinary = fillBinaryTill(outputBinary, CONTENT_OFFSET)
        else:
            outputBinary += self._trailingBinary

        sortedContent = self.getContent()
        for key, imageElement in sortedContent:
            currentOffset = len(outputBinary)
            elementOffset = int(key, 16)

            assert currentOffset <= elementOffset, "Volume content overflow for offset {} with expected offset {}".format(hex(currentOffset), hex(elementOffset))

            # Paddings between Entries
            outputBinary = fillBinaryTill(outputBinary, elementOffset)

            elementBinary = imageElement.serialize()
            EXPECTED_FILE_SIZE = imageElement.getSize()
            BINARY_SIZE = len(elementBinary)
            assert BINARY_SIZE == EXPECTED_FILE_SIZE, "File size missmatch for offset {} with size {}, expected {}".format(hex(elementOffset), hex(BINARY_SIZE), hex(EXPECTED_FILE_SIZE))
            outputBinary += elementBinary

        # Padding at the end of the directories content
        outputBinary = fillBinaryTill(outputBinary, self.getHeader().getDirectorySize())

        return outputBinary

