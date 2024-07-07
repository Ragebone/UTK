import abc

from UtkAmd.utkAmdInterfaces import UtkAMD
from UtkBase.images.imageElement import ImageElement
from utkInterfaces import Reference, Serializable


class ZenReference(Reference, UtkAMD):
    """
    Interface for references used with the PSP inside the UtkAMD module.

    """

    @classmethod
    @abc.abstractmethod
    def fromOffset(cls, absoluteOffset: int) -> 'ZenReference':
        """
        Create a reference from a "raw" offset pointing to some place in the UEFI image.

        :param absoluteOffset:
        :return: ZenReference
        """
        pass

    @abc.abstractmethod
    def getOffset(self) -> int:
        """
        Get the "raw" offset in the format the reference was created from.
        :return: raw integer including what ever was included as well on creation
        """
        pass

    @abc.abstractmethod
    def getAbsoluteOffset(self) -> int:
        """
        Get the sanitized "flash" or absolute offset.

        Useful and needed to arrive at the actual object pointed at in the image-binary
        :return: Sanitized unsigned integer that can directly be used as an offset.
        """
        pass

    @abc.abstractmethod
    def setEntry(self, entry: ImageElement) -> None:
        """
        Set the referenced entry object

        """
        pass

    @abc.abstractmethod
    def getEntry(self) -> ImageElement:
        """
        Get the referenced entry object

        """
        pass

    def followReference(self) -> Serializable:
        pass
