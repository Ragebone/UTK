import abc

from UtkBase.interfaces.serializable import serializable


class ImageElement(serializable, abc.ABC):
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

    @abc.abstractmethod
    def toString(self) -> str:
        pass
