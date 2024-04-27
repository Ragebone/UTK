from _ctypes import Structure
from ctypes import c_uint32
from typing import Any, List

from UtkAmd.uefi.images.psp.efs.efs import EmbeddedFirmwareStructure


class ZenEfs(Structure, EmbeddedFirmwareStructure):
    """
    General Embedded Firmware structure implementation for ZEN based CPUs

    References:
    https://github.com/linuxboot/fiano/blob/0ad88a5434e67ab30e2851873a33c7208cfa2db8/pkg/amd/manifest/embedded_firmware_structure.go
    https://github.com/eigenform/ragesa/blob/main/src/efs.rs
    https://github.com/PSPReverse/PSPTool/blob/master/psptool/fet.py
    """

    _fields_ = [
        ("_signature", c_uint32, 32),
        ("_imcFirmware", c_uint32, 32),
        ("_gbeFirmware", c_uint32, 32),
        ("_xHciFirmware", c_uint32, 32),
        ("_pspDirectory", c_uint32, 32),            # Legacy reference, 0x00 with anything above Zen+
        ("_pspOrComboDirectory", c_uint32, 32),
        ("_biosDirectory0", c_uint32, 32),
        ("_biosDirectory1", c_uint32, 32),
        ("_biosDirectory2", c_uint32, 32),
        ("_flags", c_uint32, 32),
        ("_biosDirectory3", c_uint32, 32),
        ("_biosDirectory4", c_uint32, 32),
        ("_promontory", c_uint32, 32),
        ("_promontoryLp", c_uint32, 32),
        ("_unknown0", c_uint32, 32),
        ("_unknown1", c_uint32, 32),
    ]

    @classmethod
    def fromBinary(cls, binary: bytes, offset: int = None) -> 'ZenEfs':
        assert binary is not None, "None as binary"
        efs = cls.from_buffer_copy(binary)
        # Set the offset like this because no idea how to otherwise set it
        efs._offset = offset
        return efs

    def __init__(self, *args: Any, **kw: Any):
        # call to the ctypes Structure so that fields get populated correctly
        super().__init__(*args, **kw)
        assert self._signature == b'\xAA\x55\xAA\x55', "ZenEfs signature missmatch, expected {}, got {}".format(b'\xAA\x55\xAA\x55', self._signature)
        self._offset: int = None

    def getSize(self) -> int:
        return len(bytes(self))

    def getDirectoryPointers(self) -> List[int]:
        """
        Get List of References to possible Directories
        :return: List of References to possible Directories
        """
        return [
            self._pspDirectory,
            self._pspOrComboDirectory,
            self._biosDirectory0,
            self._biosDirectory1,
            self._biosDirectory2,
            self._biosDirectory3,
            self._biosDirectory4,
        ]

    def getFirmwarePointers(self) -> List[int]:
        """
        Get List of References to possible firmware blobs
        :return: List of References to possible firmware
        """
        return [
            self._imcFirmware,
            self._gbeFirmware,
            self._xHciFirmware,
            self._promontory,
            self._promontoryLp
        ]

    def getOffset(self) -> int:
        return self._offset

    def toDict(self) -> dict[str, Any]:
        return {
            "offset": self._offset,
            "signature": "AA55AA55",
            "imcFirmware": self._imcFirmware,
            "gbeFirmware": self._gbeFirmware,
            "xHciFirmware": self._xHciFirmware,
            "pspDirectory": self._pspDirectory,
            "pspOrComboDirectory": self._pspOrComboDirectory,
            "biosDirectory0": self._biosDirectory0,
            "biosDirectory1": self._biosDirectory1,
            "biosDirectory2": self._biosDirectory2,
            "flags": self._flags,
            "biosDirectory3": self._biosDirectory3,
            "biosDirectory4": self._biosDirectory4,
            "promontory": self._promontory,
            "promontoryLp": self._promontoryLp,
            "unknown0": self._unknown0,
            "unknown1": self._unknown1,
        }

    def serialize(self) -> bytes:
        return bytes(self)
