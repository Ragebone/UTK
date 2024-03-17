from UtkBase.images.imageElement import ImageElement


class EmptyPadding(ImageElement):
    """
    Class to represent empty paddings in UEFI images.
    Empty meaning they only contain 0xFFs.
    Have no structures or headers identifying them.
    """

    @classmethod
    def fromBinary(cls, binary, offset):
        """
        Creates an EmptyPadding object from the binary
        Discard binary since it is just 0xFFs.
        Stores the amount bytes instead.
        :param binary:
        :param offset:
        :return:
        """
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
