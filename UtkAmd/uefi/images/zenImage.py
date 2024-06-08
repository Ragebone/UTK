import traceback

from UtkAmd.psp.firmware.firmwareFactory import FirmwareFactory
from UtkAmd.psp.directories.directory import Directory
from UtkAmd.psp.directories.directoryEntries.comboDirectoryEntry import ComboDirectoryEntry
from UtkAmd.psp.directories.directoryEntries.directoryEntry import TypedDirectoryEntry, DirectoryEntry, \
    PointDirectoryEntry
from UtkAmd.psp.directories.directoryFactory import DirectoryFactory
from UtkAmd.psp.efs.efs import EmbeddedFirmwareStructure
from UtkAmd.utkAmdInterfaces import UtkAMD
from UtkBase.images.image import Image
from UtkBase.images.imageElement import ImageElement
from UtkBase.images.paddings.paddingFactory import PaddingFactory
from UtkBase.images.volumes.volumeFactory import VolumeFactory


def resolveEfsToDirectories(efs: EmbeddedFirmwareStructure, imageBinary: bytes) -> list[Directory]:
    """
    This is supposed to build the EFS referenced directories from the given imageBinary

    Use this to get the directories from the EFS
    :param efs:
    :param imageBinary:
    :return: List of parsed Directories / ImageElements
    """
    directories = []

    # TODO  implement this with references
    for flashOffset in efs.getDirectoryPointers():
        if flashOffset == 0:
            continue

        directoryBinary = imageBinary[flashOffset:]
        # TODO the tuple index is not so nice here, improve?
        if not DirectoryFactory.isDirectory(directoryBinary)[0]:
            continue

        try:
            directory = DirectoryFactory.fromBinary(directoryBinary, flashOffset)
            directories.append(directory)
        except Exception as ex:
            from UtkBase.biosFile import BiosFile
            if BiosFile.dontHandleExceptions:
                raise ex
            traceback.print_exception(type(ex), ex, ex.__traceback__)
            continue

    return directories


def resolveDirectoryReferences(directory: Directory, imageBinary: bytes) -> list[Directory]:
    """

    :param directory:
    :param imageBinary:
    :return:
    """
    directories: list[Directory] = []
    directoryEntries: list[DirectoryEntry] = directory.getDirectoryEntries()
    for dirEntry in directoryEntries:

        if not isinstance(dirEntry, PointDirectoryEntry):
            continue

        # NOT A FLASHOFFSET
        unknownOffset = dirEntry.getEntryLocation()
        if unknownOffset & 0xFF000000 > 0:
            continue

        flashOffset = 0x00FFFFFF & unknownOffset

        if isinstance(dirEntry, ComboDirectoryEntry):
            directoryBinary = imageBinary[flashOffset:]
            directoryFromFlashOffset(directoryBinary, flashOffset, directories)

        if not isinstance(dirEntry, TypedDirectoryEntry):
            continue

        entryType = dirEntry.getEntryType()

        if entryType not in [0x40, 0x70]:
            continue

        # TODO remove redundancy
        directoryBinary = imageBinary[flashOffset:]
        # TODO the tuple index is not so nice here, improve?
        if not DirectoryFactory.isDirectory(directoryBinary)[0]:
            continue

        directoryFromFlashOffset(directoryBinary, flashOffset, directories)

    return directories


def directoryFromFlashOffset(directoryBinary: bytes, flashOffset: int, foundDirectories: list[Directory]):

    # TODO the tuple index is not so nice here, improve?
    if not DirectoryFactory.isDirectory(directoryBinary)[0]:
        return

    try:
        directory = DirectoryFactory.fromBinary(directoryBinary, flashOffset)
        foundDirectories.append(directory)
    except Exception as ex:
        from UtkBase.biosFile import BiosFile
        if BiosFile.dontHandleExceptions:
            raise ex
        traceback.print_exception(type(ex), ex, ex.__traceback__)


def resolvePointDirectoryEntries(directory: Directory, listOfImageElements: list[ImageElement], binary: bytes):
    """
    Goe through given directories dirEntries to resolve those pointing outside the directory.
    Does not follow 0x40 and 0x70 types since those are directories that need to have been built before this can be called.

    :return: Nothing
    """
    for dirEntry in directory.getDirectoryEntries():
        if not isinstance(dirEntry, TypedDirectoryEntry):
            continue

        if not dirEntry.isPointEntry:
            continue

        # psp and bios directories as well as the PEI volume
        if dirEntry.getEntryType() in [0x40, 0x70, 0x62]:
            continue

        # TODO problematic weird directory entries who's sizes and locations don't make sense yet
        if dirEntry.getEntryType() in [0x2A, 0x46]:
            continue

        if dirEntry.getEntrySize() < 1:
            # 0 sized APOB for instance
            # just skipp those for now
            continue

        # check if the firmware already exists in the imageElements
        OFFSET = dirEntry.getEntryLocation()
        if firmwareAlreadyBuilt(listOfImageElements, OFFSET, binary):
            continue

        FIRMWARE_BINARY = binary[OFFSET: OFFSET + dirEntry.getEntrySize()]
        firmware = FirmwareFactory.fromBinary(dirEntry.getEntryType(), FIRMWARE_BINARY, OFFSET)
        listOfImageElements.append(firmware)


def firmwareAlreadyBuilt(listOfImageElements: list[ImageElement], OFFSET: int, binary: bytes) -> bool:
    """
    Check through listOfImageElements whether something is present starting at the Offset.
    Or where the Offset is inside.

    :param binary:
    :param OFFSET:
    :param listOfImageElements:
    :return:
    """
    sortedImageItems = sorted(listOfImageElements, key=lambda item: item.getOffset())
    for imageElement in sortedImageItems:
        ELEMENT_OFFSET = imageElement.getOffset()
        if ELEMENT_OFFSET > OFFSET:
            # past
            break

        if ELEMENT_OFFSET <= OFFSET < ELEMENT_OFFSET + imageElement.getSize():
            # Exactly at or inside something
            return True

    return False


class ZenImage(Image, UtkAMD):
    """
    AMD ZEN specific UEFI image implementation.

    Reference: https://github.com/coreboot/coreboot/blob/master/Documentation/soc/amd/psp_integration.md
    """

    EFS_OFFSETS = [
        0x000a0000,
        0x00020000,
        0x00e20000,
        0x00c20000,
        0x00820000
        # 0xff020000
    ]

    @classmethod
    def fromBinary(cls, binary: bytes, efs: EmbeddedFirmwareStructure = None, imageOffset: int = 0) -> 'ZenImage':
        """
        Construct an AMD ZEN specific image from the given binary

        :param binary: The full image binary to make finding and parsing things from it easier.
        :param efs: Optional EmbeddedFirmwareStructure
        :param imageOffset: Optional offset where the image is located in the larger file
        :return: An GenericImage object
        """

        # 1: Getting an EFS otherwise this is not an AMD image
        if efs is None:
            pass
            # TODO search for the EFS
            # efs =

        assert efs is not None, "Must have a valid FirmwareEntryTable"

        # 2: Get the directories from the EFS
        listOfImageElements: list[ImageElement] = [efs]
        listOfDirectories: list[Directory] = []
        directoriesToBeResolved = resolveEfsToDirectories(efs, binary)

        # 3: Get directories from directories and then from those directories ...
        while len(directoriesToBeResolved) > 0:
            listOfImageElements.extend(directoriesToBeResolved)
            listOfDirectories.extend(directoriesToBeResolved)

            newList: list[Directory] = []
            for directory in directoriesToBeResolved:
                directoryEntries: list[Directory] = resolveDirectoryReferences(directory, binary)
                newList.extend(directoryEntries)

            directoriesToBeResolved = newList

        # 4: Get UEFI volumes
        offset = 0
        IMAGE_LENGTH = len(binary)
        while offset < IMAGE_LENGTH:
            from UtkBase.images.imageFactory import VOLUME_START_TO_SIGNATURE_OFFSET
            NEXT_VOLUME_OFFSET = binary.find(b'_FVH', offset) - VOLUME_START_TO_SIGNATURE_OFFSET

            if NEXT_VOLUME_OFFSET < 0:
                # No further volumes in the image
                break

            # make a volume
            offset = NEXT_VOLUME_OFFSET
            VOLUME_BINARY = binary[offset:]  # Unlimited binary, the volume has to limit itself!

            volume = VolumeFactory.fromBinary(VOLUME_BINARY, offset)

            listOfImageElements.append(volume)
            offset += volume.getSize()

        # 5: Resolve pointDirectoryEntries
        for directory in listOfDirectories:
            resolvePointDirectoryEntries(directory, listOfImageElements, binary)

        # 6 TODO Resolve EFS pointers at untyped firmware

        # 7: fill gaps in with paddings.
        sortedImageItems = sorted(listOfImageElements, key=lambda item: item.getOffset())
        paddings = []
        offset = 0
        for imageElement in sortedImageItems:
            itemOffset = imageElement.getOffset()
            if offset < itemOffset:
                # Padding between imageElements
                PADDING_BINARY = binary[offset:itemOffset]
                padding = PaddingFactory.fromBinary(PADDING_BINARY, offset)
                paddings.append(padding)

            offset = itemOffset + imageElement.getSize()

        if offset < len(binary):
            # trailing padding at the end of the image
            PADDING_BINARY = binary[offset:]
            padding = PaddingFactory.fromBinary(PADDING_BINARY, offset)
            paddings.append(padding)

        listOfImageElements.extend(paddings)

        # 8: Transfer, sort and validate everything nicely
        imageElements: dict[str, ImageElement] = {}
        sortedImageItems = sorted(listOfImageElements, key=lambda item: item.getOffset())
        for imageElement in sortedImageItems:
            ELEMENT_OFFSET = imageElement.getOffset()

            elementAtOffset = imageElements.get(hex(ELEMENT_OFFSET), None)
            assert elementAtOffset is None, "collision at offset {}".format(hex(ELEMENT_OFFSET))
            imageElements[hex(ELEMENT_OFFSET)] = imageElement

        return cls(imageElements, imageOffset)

    @classmethod
    def fromDict(cls, dictionary: dict) -> 'ZenImage':
        return cls(dictionary.get('content', {}))

    def __init__(self, contents: dict[str, ImageElement], imageOffset: int = 0):
        """
        Constructor for an AMD Image
        :param contents: Must be a dictionary sorted ascending by the key being a hex(offset) string.
        :param imageOffset: Offset where the image is inside the Bios-File
        """
        self._offset = imageOffset
        self._contents: dict[str, ImageElement] = contents

    def getSize(self):
        """
        Get the current size of the image.
        To handle changes of the image imageElements, this gets calculated every time

        :return: Int size of the image
        """
        size = 0
        for hexOffset, imageElement in self._contents.items():
            if imageElement is not None:
                size += imageElement.getSize()
        return size

    def getOffset(self) -> int:
        return self._offset

    def getContent(self) -> list[tuple[str, ImageElement]]:
        """
        Get a copy of the images content as a sorted list containing a tuple of (hex(offset), ImageElement)
        For example ("0x20000", ZenEfs)

        List gets copied and sorted every time to ensure it is ordered and can't be used to change what the image contains.

        Use this to work with the ImageElements contained in the Image.
        Do not use this to add or remove elements from the image
        """
        return sorted(self._contents.copy().items(), key=lambda item: int(item[0], 16))

    def toDict(self) -> dict[str, any]:
        return {
            "offset": self._offset,
            "content": self._contents
        }

    def serialize(self) -> bytes:
        """ Serializable """
        outputBinary = bytes()
        sortedContent = self.getContent()
        for index, (strOffset, imageElement) in enumerate(sortedContent):
            currentOffset = len(outputBinary)
            ELEMENT_OFFSET = int(strOffset, 16)

            assert currentOffset == ELEMENT_OFFSET, "Image content missmatch: Offset {} with intended {}".format(hex(currentOffset), hex(ELEMENT_OFFSET))

            elementBinary = imageElement.serialize()
            EXPECTED_SIZE = imageElement.getSize()
            BINARY_SIZE = len(elementBinary)
            assert BINARY_SIZE == EXPECTED_SIZE, "File size missmatch for offset {} with size {}, expected {}".format(hex(ELEMENT_OFFSET), hex(BINARY_SIZE), hex(EXPECTED_SIZE))
            outputBinary += elementBinary

        return outputBinary

