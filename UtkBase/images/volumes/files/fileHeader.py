import struct

from UtkBase.interfaces.serializable import serializable
from UtkBase.uefiGuid import UefiGuid

# https://github.com/tianocore/edk2/blob/4c8144dd665619731b6c3c19f4f1ae664b69fa4b/BaseTools/Source/C/Include/Common/PiFirmwareFile.h#L33
EFI_FV_FILETYPE_ALL                     = 0x00
EFI_FV_FILETYPE_RAW                     = 0x01
EFI_FV_FILETYPE_FREEFORM                = 0x02
EFI_FV_FILETYPE_SECURITY_CORE           = 0x03
EFI_FV_FILETYPE_PEI_CORE                = 0x04
EFI_FV_FILETYPE_DXE_CORE                = 0x05
EFI_FV_FILETYPE_PEIM                    = 0x06
EFI_FV_FILETYPE_DRIVER                  = 0x07
EFI_FV_FILETYPE_COMBINED_PEIM_DRIVER    = 0x08
EFI_FV_FILETYPE_APPLICATION             = 0x09
EFI_FV_FILETYPE_MM                      = 0x0A
EFI_FV_FILETYPE_FIRMWARE_VOLUME_IMAGE   = 0x0B
EFI_FV_FILETYPE_COMBINED_MM_DXE         = 0x0C
EFI_FV_FILETYPE_MM_CORE                 = 0x0D
EFI_FV_FILETYPE_MM_STANDALONE           = 0x0E
EFI_FV_FILETYPE_MM_CORE_STANDALONE      = 0x0F
EFI_FV_FILETYPE_OEM_MIN                 = 0xC0
EFI_FV_FILETYPE_OEM_MAX                 = 0xDF
EFI_FV_FILETYPE_DEBUG_MIN               = 0xE0
EFI_FV_FILETYPE_DEBUG_MAX               = 0xEF
EFI_FV_FILETYPE_PAD                     = 0xF0
EFI_FV_FILETYPE_FFS_MIN                 = 0xF0
EFI_FV_FILETYPE_FFS_MAX                 = 0xFF

#    File types
_typeMapping = {
        EFI_FV_FILETYPE_RAW:                  "Raw",
        EFI_FV_FILETYPE_FREEFORM:             "Freeform",
        EFI_FV_FILETYPE_SECURITY_CORE:        "SEC core",
        EFI_FV_FILETYPE_PEI_CORE:             "PEI core",
        EFI_FV_FILETYPE_DXE_CORE:             "DXE core",
        EFI_FV_FILETYPE_PEIM:                 "PEI module",
        EFI_FV_FILETYPE_DRIVER:               "DXE driver",
        EFI_FV_FILETYPE_COMBINED_PEIM_DRIVER: "Combined PEI/DXE",
        EFI_FV_FILETYPE_APPLICATION:          "Application",
        EFI_FV_FILETYPE_MM:                   "SMM module",
        EFI_FV_FILETYPE_FIRMWARE_VOLUME_IMAGE:"Volume image",
        EFI_FV_FILETYPE_COMBINED_MM_DXE:      "Combined SMM/DXE",
        EFI_FV_FILETYPE_MM_CORE:              "SMM core",
        EFI_FV_FILETYPE_MM_STANDALONE:        "MM standalone module",
        EFI_FV_FILETYPE_MM_CORE_STANDALONE:   "MM standalone core",
        EFI_FV_FILETYPE_PAD:                  "Pad"
}


class FileHeader(serializable):
    """
    References
    # https://github.com/LongSoft/UEFITool/blob/036be8d3bc9afb49fc9186aa5e5142df98b76586/common/basetypes.h#L181
    # https://github.com/LongSoft/UEFITool/blob/036be8d3bc9afb49fc9186aa5e5142df98b76586/common/ffs.cpp#L187
    # https://github.com/tianocore/edk2/blob/4c8144dd665619731b6c3c19f4f1ae664b69fa4b/BaseTools/Source/C/Include/Common/PiFirmwareFile.h#L33
    """
    @classmethod
    def _struct(cls):
        return struct.Struct('<16s H B B 3s B')

    @classmethod
    def fromBinary(cls, binary: bytes, **kwargs):
        guidBinary, integrityCheck, fileType, attributes, size24, state = cls._struct().unpack(binary[:cls._struct().size])
        guid = UefiGuid.fromBinary(guidBinary)
        fileSize, = struct.unpack('<I', size24 + b'\x00')
        header = cls(guid, integrityCheck, fileType, attributes, fileSize, state)
        return header

    def __init__(self, guid, integrityCheck, fileType, attributes, fileSize, state):
        self._guid = guid
        self._integrityCheck = integrityCheck
        self._fileType = fileType
        self._attributes = attributes
        self._fileSize = fileSize
        self._state = state

    def getGuid(self):
        return self._guid

    def getFileType(self):
        return self._fileType

    def getSize(self):
        return self._struct().size

    def getFileSize(self):
        return self._fileSize

    def toString(self):
        return "{:<40} type: {:<10} size: {:<15} state: {:5} tString {:25}\n".format(self._guid.toString(), hex(self._fileType), hex(self._fileSize), hex(self._state), _typeMapping.get(self._fileType, "unknown"))

    def serialize(self):
        guidBinary = self._guid.serialize()
        size24 = struct.pack('<I', self._fileSize)[:3]
        return self._struct().pack(guidBinary, self._integrityCheck, self._fileType, self._attributes, size24, self._state)

