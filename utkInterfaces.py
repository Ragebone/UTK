import abc
from typing import Any


class Serializable:
    """
    Interface for everything that is or is within actual firmware.

    Needed to reverse parsing; Conversion back to usable firmware.
    And as intermediate step for:
    - Exporting
    - Importing
    - Printing
    - ?
    """
    @abc.abstractmethod
    def serialize(self) -> bytes:
        """
        Serialize object back to binary / bytes usable in or as firmware.

        :return: bytes: The serialized object as bytes
        """
        pass

    @abc.abstractmethod
    def toDict(self) -> dict[str, Any]:
        """
        Convert object to an intermediate format; A dictionary.
        Attribute-names are keys.
        Attribute values are the dict-values.

        Mainly useful as an intermediate step for conversions, exports, imports and yet unknown features.
        Instead of having to implement a bunch of "toSomething" and "fromSomething" functions,
        we can just use the dict instead.
        This could also be considered a "closed door, open door" implementation.

        NOTE: Dict values being objects, makes it harder to convert this to json.
        Use a fitting converter-strategy for this

        :return: Dictionary of the objects attributes
        """
        pass


class Header(Serializable):
    """
    Interface / abstract class to identify objects that are considered "headers".

    Usefully for extracting or printing headers differently.
    For choosing "strategies" depending on such types.

    Intended to be the one thing all headers have in common
    """
    pass


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
