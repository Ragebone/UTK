import abc

from UtkBase.interfaces.serializable import serializable


class Image(serializable, abc.ABC):

    @abc.abstractmethod
    def getSize(self) -> int:
        pass

    @abc.abstractmethod
    def toString(self) -> str:
        pass
