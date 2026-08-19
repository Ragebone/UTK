import abc

from UtkAmd.psp.directories.directory import Directory, CONTENT_OFFSET, DIRECTORY_MINIMUM_SIZE_BLOCK_ALIGNMENT_THINGY
from UtkAmd.psp.directories.directoryEntries.directoryEntry import TypedDirectoryEntry
from UtkAmd.psp.firmwareTypes import MODIFIABLE_FIRMWARE_TYPES
from UtkAmd.psp.zenReference import ZenReference
from UtkBase import utility
from UtkBase.images.imageElement import ImageElement


class BuildStrategy:
    """


    """
    @abc.abstractmethod
    @staticmethod
    def buildDirectoryContent(directory: Directory) -> None:
        pass


class AbsoluteInImage(BuildStrategy):
    """


    """
    @staticmethod
    def buildDirectoryContent(directory: Directory) -> None:
        directory.rebuildDirectoryRelative()
        directory.calculateNewDirectoryEntryOffsets()


class RelativeInPartition(BuildStrategy):
    """


    """

    @staticmethod
    def buildDirectoryContent(directory: Directory) -> None:
        """
        RelativeInPartition.buildDirectoryContent(directory)

        NOT SUPPORTED YET

        Unclear what a Partition is and how to determine those details from inside or around the directory.
        :param directory:
        :return:
        """
        # 0 Relative build through
        # RelativeInDirectory.buildDirectoryContent(directory)

        # 1 find the partition
        # 2 possibly change / rebuild the partition, in case it needs to be made larger for instance
        # 3 with that calculate the addition to the relative offsets
        # 4 add this offset to the directory relative content
        # ? set AddressModes correctly on the Directory and References
        # X cool references and finalize the Image

        return NotImplementedError


class RelativeInDirectory(BuildStrategy):
    """


    """
    @staticmethod
    def buildDirectoryContent(directory: Directory) -> None:
        endOfContent, directoryContent = arrangeDirectoryContent(directory)

        ALIGNED_END_OF_DIRECTORY = utility.alignOffset(endOfContent, DIRECTORY_MINIMUM_SIZE_BLOCK_ALIGNMENT_THINGY)

        if ALIGNED_END_OF_DIRECTORY > directory.getSize():
            assert False, "New Directory-content exceeded available space in Directory. TODO support for enlarging"
            # Directory too small
            directory.getHeader().setDirectorySize(ALIGNED_END_OF_DIRECTORY)
            # TODO mark the directory as changed
            # TODO tell its parent so that the Directory can be re-fitted into the image
            # TODO enlarge directory

        # -----
        # Here it is to be expected that the Directory now was placed correctly and that its offset is correct.

        directoryOffset = directory.getOffset()
        sortedContent: list[tuple[str, ImageElement]] = sorted(self._content.items(), key=lambda item: int(item[0], 16))

        for offset, firmwareEntry in sortedContent:

            references: list[Reference] = firmwareEntry.getReferences()

            for reference in references:
                # TODO  check if the Reference is in this directory.
                # If yes, since we are Relative to inside the Directory, just set the offset value of the reference to this offset.
                # IF outside, we need to calculate the image-absolute offset of the entry and set that.
                # so  this "hex(offset)"  + directory.getOffset()
                # set that to the

                if not isinstance(reference, ZenReference):
                    continue

                reference: ZenReference

                parent = reference.getParent()
                if isinstance(parent, DirectoryEntry):
                    parent = parent.getParent()

                if isinstance(parent, Directory):
                    if parent == directory:
                        continue

                # TODO update the reference to be absolute
                reference.setAbsoluteOffset()
                # reference


def arrangeDirectoryContent(directory: Directory) -> tuple[int, dict]:
    """

    NOTE: the offset keys in the dict are hex strings and relative to the directory.
    The start at 0x400
    This is unpermanent, this just a new dict without consequences yet.
    The directory would also only that large

    :param directory:
    :return:
    """
    directoryContent: dict[str, ImageElement] = {}

    offset = CONTENT_OFFSET
    for dirEntry in directory.getDirectoryEntries():

        if not isinstance(dirEntry, TypedDirectoryEntry):
            continue

        if dirEntry.isPointEntry():
            # something outside the actual directory-container
            continue

        blockSize = 0x100
        if dirEntry.getEntryType() in MODIFIABLE_FIRMWARE_TYPES:
            blockSize = directory.getHeader().getSpiBlockSize()

        newEntryOffset = utility.alignOffset(offset, blockSize)

        reference = dirEntry.getEntryReference()

        # NOTE / TODO   the supposed entryOffset is supposed to be different here on after.
        # But it isn't set here.
        # It needs to be actually set on the Firmware, the references etc and its specific values
        # depend where the reference is and what addressMode it has
        reference.setHeat(True)
        firmware = reference.getEntry()

        directoryContent[hex(newEntryOffset)] = firmware

        offset = newEntryOffset + firmware.getSize()

    END_OF_DIRECTORY_CONTENT = offset
    return END_OF_DIRECTORY_CONTENT, directoryContent
