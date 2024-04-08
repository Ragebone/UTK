import abc

from UtkBase.capsules.headers.headerInterface import CapsuleHeader
from utkInterfaces import Serializable


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

    @classmethod
    @abc.abstractmethod
    def fromBinary(cls, binary, header: CapsuleHeader = None, offset: int = 0) -> 'Capsule':
        """
        Create a new Capsule from the given binary
        Optional Header and offset can be passed.

        :param binary: Bytes to build the capsule from.
        :param header: CapsuleHeader that might have been passed before.
        :param offset: Informative offset where the capsule is located inside the parent.
        Defaults to 0.
        :return: The constructed Capsule.
        """
        pass
