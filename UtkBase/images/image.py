import abc

from UtkBase.images.imageElement import ImageElement
from utkInterfaces import Serializable


class Image(Serializable):
    """
    Interface for UEFI Image implementations
    Methods and functionality they all have in common
    """

    @abc.abstractmethod
    def getSize(self) -> int:
        """Get the images size"""
        pass

    @abc.abstractmethod
    def getOffset(self) -> int:
        """Get the offset it is located at inside the BiosFile"""
        pass
