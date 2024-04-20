import abc
from typing import List

from UtkAmd.utkAmdInterfaces import AMD
# TODO this dependency is fine but should be pulled out somewhere else maybe?
from UtkBase.images.imageElement import ImageElement


class EmbeddedFirmwareStructure(ImageElement, AMD, abc.ABC):
    """
    ABC / Interface for all EFSs
    """

    @abc.abstractmethod
    def getOffset(self) -> int:
        pass

    @abc.abstractmethod
    def getSize(self) -> int:
        pass

    @abc.abstractmethod
    def getDirectoryPointers(self) -> List[int]:
        pass
