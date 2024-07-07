import abc

from utkInterfaces import Serializable, Header, Reference


class ImageElement(Serializable):
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
    def fromBinary(cls, binary: bytes, header: Header = None, offset: int = 0, *kwargs) -> 'ImageElement':
        pass

    @abc.abstractmethod
    def registerReference(self, reference: Reference) -> None:
        """
        Register the given Reference-Object with this ImageElement.

        Needed for updating references when the ImageElement changes location.
        Or as a way to get from the ImageElement to all places that reference it by offset.

        :param reference: The reference referring to this object
        :return: None Nothing, this can't fail
        """
        pass

    @abc.abstractmethod
    def getReferences(self) -> list[Reference]:
        """
        Get all references registered with this ImageElement.

        Useful as a way to get from the ImageElement to all places that reference it by offset.
        TODO  deliberate if this should be a copy of the list and not the list itself
        :return: The list of references registered with this ImageElement
        """
        pass
