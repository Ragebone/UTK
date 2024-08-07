from UtkAmd.psp.addressMode import AddressMode
from UtkAmd.psp.zenReference import ZenReference
from UtkBase.images.imageElement import ImageElement


class EfsReference(ZenReference):
    """
    Reference implementation for 32 Bit based offsets used in EFSs.

    """

    @classmethod
    def fromOffset(cls, offset: int) -> 'EfsReference':
        mode = AddressMode.PhysicalX86

        if offset & 0xFF000000 != 0xFF000000:
            # flash-offset
            mode = AddressMode.FlashOffset

        return cls(offset, mode)

    def __init__(self, absoluteOffset: int, addressMode: AddressMode):
        self._offset = absoluteOffset
        self._addressMode = addressMode

        self._linkedObject = None

    def getOffset(self) -> int:
        return self._offset

    def getAbsoluteOffset(self):
        if self._addressMode == AddressMode.FlashOffset:
            return self._offset

        return self._offset & 0x00FFFFFF

    def setEntry(self, entry: ImageElement) -> None:
        self._linkedObject = entry

    def getEntry(self) -> ImageElement:
        return self._linkedObject
