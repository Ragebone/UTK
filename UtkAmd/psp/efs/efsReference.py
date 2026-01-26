from UtkAmd.psp.addressMode import AddressMode
from UtkAmd.psp.zenReference import ZenReference
from UtkBase.images.imageElement import ImageElement
from utkInterfaces import Serializable


class EfsReference(ZenReference):
    """
    Reference implementation for 32 Bit based offsets used in EFSs.

    """

    @classmethod
    def fromOffset(cls, offset: int, parent: 'EmbeddedFirmwareStructure') -> 'EfsReference':
        mode = AddressMode.PhysicalX86

        if offset & 0xFF000000 != 0xFF000000:
            # flash-offset
            mode = AddressMode.FlashOffset

        return cls(offset, mode, parent)

    def __init__(self, absoluteOffset: int, addressMode: AddressMode, parent: 'EmbeddedFirmwareStructure'):
        self._offset = absoluteOffset
        self._addressMode = addressMode

        self._linkedObject = None

        self._hot = False

        self._parent = parent

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

    def followReference(self) -> Serializable:
        return self._linkedObject

    def setParent(self, parent) -> None:
        self._parent = parent

    def getParent(self) -> ImageElement:
        return self._parent

    def setAbsoluteOffset(self, absoluteOffset: int) -> None:
        pass

    def setHeat(self, hot: bool = True) -> None:
        """

        :param hot:
        :return:
        """
        self._hot = hot

    def isHot(self) -> bool:
        return self._hot
