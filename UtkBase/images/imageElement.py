import abc

from UtkBase.images.volumes.headers.volumeHeader import VolumeHeader
from interfaces import Serializable


class ImageElement(Serializable, abc.ABC):
    """
    Interface for elements contained directly within the UEFI image.
    Mainly Paddings and UEFI volumes.
    OEMs like AMD and Intel have their own special additions
    """

    @abc.abstractmethod
    def getSize(self) -> int:
        pass

    @abc.abstractmethod
    def getOffset(self) -> int:
        pass

    @classmethod
    @abc.abstractmethod
    def fromBinary(cls, binary: bytes, header: VolumeHeader = None, volumeOffset: int = 0) -> 'Volume':
        pass
