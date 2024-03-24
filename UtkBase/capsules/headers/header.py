import abc

from interfaces import Serializable


class CapsuleHeader(Serializable, abc.ABC):

    @abc.abstractmethod
    def getSize(self) -> int:
        pass

    @abc.abstractmethod
    def getCapsuleSize(self) -> int:
        pass

    @abc.abstractmethod
    def getEncapsulatedImageSize(self) -> int:
        pass
