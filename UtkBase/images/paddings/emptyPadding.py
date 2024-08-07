from UtkBase.images.imageElement import ImageElement
from UtkBase.utility import binaryIsEmpty
from utkInterfaces import Reference


class EmptyPadding(ImageElement):
    """
    Class to represent empty paddings in UEFI images.
    Empty meaning they only contain 0xFFs.
    Have no structures or headers identifying them.
    """

    @classmethod
    def fromBinary(cls, binary: bytes, offset: int):
        """
        Creates an EmptyPadding object from the binary
        Discard binary since it is just 0xFFs.
        Stores the amount bytes instead.
        :param binary:
        :param offset:
        :return:
        """
        length = len(binary)
        assert binaryIsEmpty(binary), "Binary must be 0xFFs for empty padding"
        return cls(length, offset)

    def __init__(self, length, offset):
        self._length = length
        self._offset = offset

        self._references: list[Reference] = []

    def registerReference(self, reference: Reference) -> None:
        self._references.append(reference)

    def getReferences(self) -> list[Reference]:
        return self._references

    def getOffset(self) -> int:
        return self._offset

    def getSize(self) -> int:
        return self._length

    def toDict(self) -> dict[str, any]:
        return {
            "size": self._length,
            "offset": self._offset
        }

    def toString(self):
        return ""

    def serialize(self) -> bytes:
        return b'\xFF' * self._length
