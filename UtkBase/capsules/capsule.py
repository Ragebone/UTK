import abc

from interfaces import Serializable


class Capsule(Serializable, abc.ABC):
    """
    Interface for all Capsul implementations
    """
    @abc.abstractmethod
    def getSize(self) -> int:
        pass

    @abc.abstractmethod
    def getImageSize(self) -> int:
        pass
