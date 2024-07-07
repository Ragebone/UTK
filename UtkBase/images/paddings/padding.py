from UtkBase.images.imageElement import ImageElement
from utkInterfaces import Reference


class Padding(ImageElement):
    @classmethod
    def fromBinary(cls, binary, offset: int = None) -> 'Padding':
        return cls(binary, offset)

    def __init__(self, binary, offset: int = None):
        self._binary = binary
        self._size = len(binary)
        self._offset = offset

        self._references: list[Reference] = []

    def registerReference(self, reference: Reference) -> None:
        self._references.append(reference)

    def getReferences(self) -> list[Reference]:
        return self._references

    def getOffset(self) -> int:
        return self._offset

    def getSize(self) -> int:
        return self._size

    def toDict(self) -> dict[str, any]:
        return {
            "size": self._size,
            "offset": self._offset,
            "binary": self._binary
        }

    def toString(self):
        return ""

    def serialize(self) -> bytes:
        return self._binary
