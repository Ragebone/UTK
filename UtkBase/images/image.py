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

    @classmethod
    @abc.abstractmethod
    def fromImageElements(cls, contents: List[ImageElement]) -> 'Image':
        pass

    @classmethod
    @abc.abstractmethod
    def fromDict(cls, dictionary: dict) -> 'Image':
        pass
