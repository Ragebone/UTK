import struct


class Block:
    @staticmethod
    def _struct():
        return struct.Struct('<II')

    @classmethod
    def fromBinary(cls, binary: bytes):
        return cls(*cls._struct().unpack(binary[:cls._struct().size]))

    def __init__(self, count, blockSize):
        self._count = count
        self._blockSize = blockSize

    def getSize(self):
        return self._struct().size

    def getCount(self):
        return self._count

    def getBlockSize(self):
        return self._blockSize

    def serialize(self):
        return self._struct().pack(self._count, self._blockSize)

    def toString(self):
        return "Block count: {}, Block size: {}\n".format(self._count, hex(self._blockSize))
