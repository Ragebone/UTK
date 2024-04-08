import abc

from utkInterfaces import Header


class CapsuleHeader(Header, abc.ABC):

    @abc.abstractmethod
    def getSize(self) -> int:
        pass

    @abc.abstractmethod
    def getCapsuleSize(self) -> int:
        pass

    @abc.abstractmethod
    def getEncapsulatedImageSize(self) -> int:
        pass
