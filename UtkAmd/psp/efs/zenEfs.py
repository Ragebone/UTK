import struct

from UtkAmd.psp.efs.efs import EmbeddedFirmwareStructure
from UtkAmd.psp.efs.efsReference import EfsReference


class ZenEfs(EmbeddedFirmwareStructure):
    """
    AMD Embedded Firmware structure implementation for ZEN based CPUs

    have a look at this:
    https://github.com/linuxboot/fiano/blob/0ad88a5434e67ab30e2851873a33c7208cfa2db8/pkg/amd/manifest/embedded_firmware_structure.go

    https://github.com/openSIL/AGCL-R/blob/c1789df006acab5e1ac1c52ec114c3de2230f54b/AgesaPkg/Include/AmdPspDirectory.h#L231

    """

    @classmethod
    def _signature(cls) -> bytes:
        return b'\xAA\x55\xAA\x55'

    @classmethod
    def _struct(cls) -> struct:
        """

        :return:
        """
        return struct.Struct('<4s IIII IIII 64s')

    @classmethod
    def fromBinary(cls, binary: bytes, offset: int = None) -> 'ZenEfs':
        assert binary is not None, "None as binary"
        return cls(offset, *cls._struct().unpack(binary[:cls._struct().size]))

    def __init__(self,
                offset: int,        # not part of the structure

                signature: bytes,
                imcFirmware: int,
                gbeFirmware: int,
                xHciFirmware: int,
                pspDirectory: int,

                pspOrComboDirectory: int,
                biosDirectory0: int,
                biosDirectory1: int,
                biosOrComboDirectory: int,

                unknownTrailingBinary: bytes):

        super().__init__()
        assert signature == self._signature(), "ZenEfs signature missmatch, expected {}, got {}".format(
            self._signature().hex().upper(), signature.hex().upper()
        )

        # TODO   one problem is    all "references" / offsets here are 32 bit and are hence different to the ones used in directories

        self._offset: int = offset

        self._imcFirmware = EfsReference.fromOffset(imcFirmware, self)
        self._gbeFirmware = EfsReference.fromOffset(gbeFirmware, self)
        self._xHciFirmware = EfsReference.fromOffset(xHciFirmware, self)
        self._pspDirectory = EfsReference.fromOffset(pspDirectory, self)                      # used with Naples and other Zen1(+)

        self._pspOrComboDirectory = EfsReference.fromOffset(pspOrComboDirectory, self)
        self._biosDirectory0 = EfsReference.fromOffset(biosDirectory0, self)
        self._biosDirectory1 = EfsReference.fromOffset(biosDirectory1, self)
        self._biosOrComboDirectory = EfsReference.fromOffset(biosOrComboDirectory, self)

        self._unknownTrailingBinary = unknownTrailingBinary

    def validate(self) -> bool:
        return True

    def getSize(self) -> int:
        return self._struct().size

    def getDirectoryPointers(self) -> list[EfsReference]:
        """
        Get List of References to possible Directories
        :return: List of References to possible Directories
        """
        return [
            # self._imcFirmware,
            # self._gbeFirmware,
            # self._xHciFirmware,
            self._pspDirectory,

            self._pspOrComboDirectory,
            self._biosDirectory0,
            self._biosDirectory1,
            self._biosOrComboDirectory
        ]

    def getFirmwarePointers(self) -> list[EfsReference]:
        """
        Get List of References to possible firmware blobs
        :return: List of References to possible firmware
        """
        return [
            self._imcFirmware,
            self._gbeFirmware,
            self._xHciFirmware,
            #self._pspDirectory,

            #self._pspOrComboDirectory,
            #self._biosDirectory0,
            #self._biosDirectory1,
            #self._biosOrComboDirectory
        ]

    def getOffset(self) -> int:
        return self._offset

    def toDict(self) -> dict[str, any]:
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
            "biosOrComboDirectory": self._biosOrComboDirectory,
            "unknownTrailingBinary": self._unknownTrailingBinary,
        }

    def serialize(self) -> bytes:
        return self._struct().pack(
            self._signature(),
            self._imcFirmware.getOffset(),
            self._gbeFirmware.getOffset(),
            self._xHciFirmware.getOffset(),
            self._pspDirectory.getOffset(),
            self._pspOrComboDirectory.getOffset(),
            self._biosDirectory0.getOffset(),
            self._biosDirectory1.getOffset(),
            self._biosOrComboDirectory.getOffset(),
            self._unknownTrailingBinary
        )

