from typing import Any

from UtkBase.images.volumes.files.fileHeader import FileHeader
from interfaces import Serializable


class File(Serializable):
    """
    Basic File implementation
    made up of a valid header and an otherwise unspecified binary content.
    Paddings and Raw-Files are the obvious files that qualify.
    """

    @classmethod
    def fromBinary(cls, binary: bytes, header: FileHeader = None) -> 'File':
        """

        :param binary:
        :param header:
        :return:
        """

        if header is None:
            header = FileHeader.fromBinary(binary)

        assert header is not None, "No FileHeader from binary: {}".format(
            binary[:256]
        )

        FILE_SIZE = header.getFileSize()
        HEADER_SIZE = header.getSize()

        # Limit binary to the Filesize and exclude the header
        binary = binary[HEADER_SIZE:FILE_SIZE]

        BINARY_SIZE = len(binary)
        assert BINARY_SIZE == FILE_SIZE - HEADER_SIZE, "File size {} missmatch with binary size {}".format(hex(FILE_SIZE), hex(BINARY_SIZE))

        file = cls(header, binary)
        return file

    def __init__(self, header: FileHeader, binary: bytes):
        self._header = header
        self._binary = binary

    def getSize(self) -> int:
        return self._header.getFileSize()

    def toDict(self) -> dict[str, Any]:
        return {
            "class": self.__class__.__name__,
            "fileHeader": self._header,
            "binary": self._binary
        }

    def toString(self) -> str:
        return "{}".format(self._header.toString())

    def serialize(self) -> bytes:
        binary = self._header.serialize()
        binary += self._binary
        return binary
