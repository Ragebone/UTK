import abc

from UtkCommon.interfaces.serializable import Serializable


class Header(Serializable):
    """
    Interface / abstract class to identify objects that are considered "headers".

    Usefully for extracting or printing headers differently.
    For choosing "strategies" depending on such types.

    Intended to be the one thing all headers have in common
    """
    @abc.abstractmethod
    def getSize(self) -> int:
        """Get the headers size"""
        pass
