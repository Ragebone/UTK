from UtkBase.images.imageElement import ImageElement


class EmptyPadding(ImageElement):

    @classmethod
    def fromBinary(cls, binary, offset):
        length = len(binary)
        return cls(length, offset)

    def __init__(self, length, offset):
        self._length = length
        self._offset = offset

    def getOffset(self) -> int:
        return self._offset

    def getSize(self) -> int:
        return self._length

    def toString(self):
        return ""

    def serialize(self) -> bytes:
        return b'\xFF' * self._length
