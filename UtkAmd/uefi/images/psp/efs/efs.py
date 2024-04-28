import abc
from typing import List

from UtkAmd.utkAmdInterfaces import AMD
from UtkBase.images.imageElement import ImageElement


class EmbeddedFirmwareStructure(ImageElement, AMD):
    """
    Interface all EFSs have to implement
    """

    @abc.abstractmethod
    def getOffset(self) -> int:
        """Get the offset / location of the EFS"""
        pass

    @abc.abstractmethod
    def getSize(self) -> int:
        """Get the size of the EFS in number of bytes"""
        pass

    @abc.abstractmethod
    def getDirectoryPointers(self) -> List[int]:
        """
        Get a list of all the offsets pointed at by the EFS that directories could be located at.

        :return: List of int offsets relative to the start of the AmdImage
        """
        pass

    @abc.abstractmethod
    def getFirmwarePointers(self) -> List[int]:
        """
        Get List of References to possible firmware blobs

        :return: List of References to possible firmware
        """
        pass
