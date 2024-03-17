import abc

from UtkBase.interfaces.serializable import serializable


class CapsuleHeader(serializable, abc.ABC):

    @abc.abstractmethod
    def getSize(self) -> int:
        pass

    @abc.abstractmethod
    def getCapsuleSize(self) -> int:
        pass

    @abc.abstractmethod
    def getEncapsulatedImageSize(self) -> int:
        pass

    @abc.abstractmethod
    def toJson(self, depth: int = 0) -> str:
        pass
