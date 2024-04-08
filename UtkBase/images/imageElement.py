import abc

from utkInterfaces import Serializable, Header


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
    def fromBinary(cls, binary: bytes, header: Header = None, offset: int = 0) -> 'ImageElement':
        pass
