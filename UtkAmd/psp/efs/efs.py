import abc

from UtkAmd.psp.efs.efsReference import EfsReference
from UtkAmd.utkAmdInterfaces import UtkAMD
from UtkBase.images.imageElement import ImageElement


class EmbeddedFirmwareStructure(ImageElement, UtkAMD):
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
    def getDirectoryPointers(self) -> list[EfsReference]:
        """
        Get a list of all the offsets pointed at by the EFS that directories could be located at.

        :return: List of int offsets relative to the start of the AmdImage
        """
        pass

    @abc.abstractmethod
    def getFirmwarePointers(self) -> list[EfsReference]:
        """
        Get List of References to possible firmware blobs

        :return: List of References to possible firmware
        """
        pass
