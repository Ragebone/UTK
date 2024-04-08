import abc
from typing import List

from UtkBase.images.imageElement import ImageElement
from interfaces import Serializable


class Image(Serializable, abc.ABC):
    """
    Interface for UEFI Image implementations
    """

    @abc.abstractmethod
    def getSize(self) -> int:
        pass

    @abc.abstractmethod
    def getOffset(self) -> int:
        pass

    @abc.abstractmethod
    def getContents(self) -> List[ImageElement]:
        pass

    @classmethod
    @abc.abstractmethod
    def fromImageElements(cls, contents: List[ImageElement], binary: bytes) -> 'Image':
        pass

    @classmethod
    @abc.abstractmethod
    def fromDict(cls, dictionary: dict) -> 'Image':
        pass
