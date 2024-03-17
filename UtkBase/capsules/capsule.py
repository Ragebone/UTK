import abc

from UtkBase.interfaces.serializable import serializable


class Capsule(serializable, abc.ABC):
    """
    Interface for all Capsul implementations
    """
    @abc.abstractmethod
    def getSize(self) -> int:
        pass

    @abc.abstractmethod
    def getImageSize(self) -> int:
        pass

    @abc.abstractmethod
    def toJson(self, depth: int = 0) -> str:
        pass
