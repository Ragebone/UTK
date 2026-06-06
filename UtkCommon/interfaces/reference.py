import abc

from UtkCommon.interfaces.serializable import Serializable


class Reference:
    """
    Interface for references inside the UTK

    References inside UEFI images and especially AMD firmware structures are simply "offsets" with 0 being the start as the Image.
    But there are some issues with that:
    Moving the referenced objects requires the "offset" to change as well.
    Some Offsets are not meant to start at the top of the UEFI image.
    Some offsets are relative to something.
    Some offsets require special formats and masking, unmasking or padding.

    Multiple structures can reference the same thing requiring different formats.

    This Interface is supposed to:
    - declare and enforce common functionality
    - Provide a simple way to detect such references to allow special treatment

    Problems:
    UtkAMD PSP ZenReferences are based on offsets.
    UtkBase / Uefi references are probably mostly GUID based.
    """
    @abc.abstractmethod
    def followReference(self) -> Serializable:
        """
        A reference always refers to something.
        This method is for getting or following this to the object.

        :return: Gives you the object or None if there is nothing
        """

        pass

    @abc.abstractmethod
    def getParent(self) -> any:
        pass
