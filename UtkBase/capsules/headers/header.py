import abc

from UtkBase.interfaces.serializable import serializable, serializeAsJsonFile


class CapsuleHeader(serializable, serializeAsJsonFile, abc.ABC):

    @abc.abstractmethod
    def getSize(self) -> int:
        pass

    @abc.abstractmethod
    def getCapsuleSize(self) -> int:
        pass

    @abc.abstractmethod
    def getEncapsulatedImageSize(self) -> int:
        pass
