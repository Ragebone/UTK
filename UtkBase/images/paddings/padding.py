from UtkBase.images.imageElement import ImageElement


class Padding(ImageElement):
    @classmethod
    def fromBinary(cls, binary, offset: int = None) -> 'Padding':
        return cls(binary, offset)

    def __init__(self, binary, offset: int = None):
        self._binary = binary
        self._size = len(binary)
        self._offset = offset

    def getOffset(self) -> int:
        return self._offset

    def getSize(self) -> int:
        return self._size

    def toString(self):
        return ""

    def serialize(self) -> bytes:
        return self._binary
