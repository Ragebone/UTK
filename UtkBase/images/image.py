import abc

from UtkBase.interfaces.serializable import serializable


class Image(serializable, abc.ABC):
    """
    Interface for UEFI Image implementations
    """

    @abc.abstractmethod
    def getSize(self) -> int:
        pass
