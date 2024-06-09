import struct

from UtkBase.images.volumes.files.type import EfiFirmwareFileType
from UtkBase.uefiGuid import UefiGuid
from utkInterfaces import Header


class FileHeader(Header):
    """
    References
    # https://github.com/LongSoft/UEFITool/blob/036be8d3bc9afb49fc9186aa5e5142df98b76586/common/basetypes.h#L181
    # https://github.com/LongSoft/UEFITool/blob/036be8d3bc9afb49fc9186aa5e5142df98b76586/common/ffs.cpp#L187
    # https://github.com/tianocore/edk2/blob/4c8144dd665619731b6c3c19f4f1ae664b69fa4b/BaseTools/Source/C/Include/Common/PiFirmwareFile.h#L33
    """
    @classmethod
    def _struct(cls) -> struct:
        return struct.Struct('<16s H B B 3s B')

    @classmethod
    def size(cls) -> int:
        return cls._struct().size

    @classmethod
    def fromBinary(cls, binary: bytes) -> 'FileHeader':
        HEADER_BINARY = binary[:cls._struct().size]
        assert len(HEADER_BINARY) == cls._struct().size, "Binary size missmatch"
        guidBinary, integrityCheck, intFileType, attributes, size24, state = cls._struct().unpack(HEADER_BINARY)
        guid = UefiGuid.fromBinary(guidBinary)
        fileType = EfiFirmwareFileType(intFileType)
        fileSize, = struct.unpack('<I', size24 + b'\x00')
        header = cls(guid, integrityCheck, fileType, attributes, fileSize, state)
        return header

    def __init__(self, guid: UefiGuid, integrityCheck: int, fileType: EfiFirmwareFileType, attributes: int, fileSize: int, state: int):
        self._guid = guid
        self._integrityCheck = integrityCheck
        self._fileType = fileType
        self._attributes = attributes
        self._fileSize = fileSize
        self._state = state

    def getGuid(self) -> UefiGuid:
        return self._guid

    def getFileType(self) -> EfiFirmwareFileType:
        return self._fileType

    def getSize(self) -> int:
        return self._struct().size

    def getFileSize(self) -> int:
        return self._fileSize

    def toDict(self) -> dict[str, any]:
        return {
            "guid": self._guid,
            "integrityCheck": self._integrityCheck,
            "fileType": self._fileType,
            "attributes": self._attributes,
            "fileSize": self._fileSize,
            "state": self._state
        }

    def toString(self) -> str:
        return "{:<40} type: {:<10} size: {:<15} state: {:5} tString {:25}\n".format(self._guid.toString(), hex(self._fileType.value), hex(self._fileSize), hex(self._state), self._fileType.name)

    def serialize(self) -> bytes:
        guidBinary = self._guid.serialize()
        size24 = struct.pack('<I', self._fileSize)[:3]
        return self._struct().pack(guidBinary, self._integrityCheck, self._fileType.value, self._attributes, size24, self._state)

