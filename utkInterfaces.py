import abc
from typing import Any


class Serializable(abc.ABC):
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


class Header(Serializable, abc.ABC):
    """
    Interface / abstract class to identify objects that are considered "headers".

    Usefully for extracting or printing headers differently.
    For choosing "strategies" depending on such types.

    Intended to be the one thing all headers have in common
    """
    pass
