from UtkAmd.psp.addressMode import AddressMode
from UtkAmd.psp.zenReference import ZenReference
from UtkAmd.utkAmdInterfaces import UtkAMD
from UtkBase.images.imageElement import ImageElement


class EntryReference(ZenReference, UtkAMD):
    """
    Implementation of References used in DirectoryEntries

    """

    @classmethod
    def fromOffset(cls, offset: int, modeOverride: AddressMode = None) -> 'EntryReference':
        """
        Create a reference specific to EFS structures.

        :param modeOverride:
        :param offset:
        :return:
        """

        if modeOverride is not None:
            return cls(offset, modeOverride)

        # Need to determine the mode here manually
        MODE_INT = offset >> 62
        mode = AddressMode(MODE_INT)

        if mode != AddressMode.PhysicalX86:
            return cls(offset, mode)

        # physical x86 exceptions
        if offset & 0xFF000000 != 0xFF000000:
            return cls(offset, AddressMode.FlashOffset)

        return cls(offset, mode)

    def __init__(self, absoluteOffset: int, addressMode: AddressMode):

        self._offset = absoluteOffset
        self._addressMode = addressMode

        self._linkedObject = None

    def getOffset(self) -> int:
        """
        Get the offset in its original format.

        :return:
        """
        return self._offset

    def getAbsoluteOffset(self):
        """

        :return:
        """
        if self._addressMode == AddressMode.FlashOffset:
            return self._offset & 0x3FFFFFFFFFFFFFFF        # Mask off the mode

        return self._offset & 0x00FFFFFF

    def setEntry(self, entry: ImageElement) -> None:
        self._linkedObject = entry

    def getEntry(self) -> ImageElement:
        return self._linkedObject
