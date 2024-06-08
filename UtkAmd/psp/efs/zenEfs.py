import struct

from UtkAmd.psp.efs.efs import EmbeddedFirmwareStructure
from UtkAmd.psp.efs.efsReference import EfsReference


class ZenEfs(EmbeddedFirmwareStructure):
    """
    AMD Embedded Firmware structure implementation for ZEN based CPUs

    have a look at this:
    https://github.com/linuxboot/fiano/blob/0ad88a5434e67ab30e2851873a33c7208cfa2db8/pkg/amd/manifest/embedded_firmware_structure.go

    https://github.com/openSIL/AGCL-R/blob/c1789df006acab5e1ac1c52ec114c3de2230f54b/AgesaPkg/Include/AmdPspDirectory.h#L231
    /// Unified Boot BIOS Directory structure
    enum _BIOS_DIRECTORY_ENTRY_TYPE {
      BIOS_PUBLIC_KEY               = 0x05,       ///< PSP entry points to BIOS public key stored in SPI space
      BIOS_RTM_SIGNATURE            = 0x07,       ///< PSP entry points to signed BIOS RTM hash stored  in SPI space
      MAN_OS                        = 0x5C,       ///< PSP entry points to manageability OS binary
      MAN_IP_LIB                    = 0x5D,       ///< PSP entry points to manageability proprietary IP library
      MAN_CONFIG                    = 0x5E,       ///< PSP entry points to manageability configuration inforamtion
      BIOS_APCB_INFO                = 0x60,       ///< Agesa PSP Customization Block (APCB)
      BIOS_APOB_INFO                = 0x61,       ///< Agesa PSP Output Block (APOB) target location
      BIOS_FIRMWARE                 = 0x62,       ///< BIOS Firmware volumes
      APOB_NV_COPY                  = 0x63,       ///< APOB data copy on non-volatile storage which will used by ABL during S3 resume
      PMU_INSTRUCTION               = 0x64,       ///< Location field pointing to the instruction portion of PMU firmware
      PMU_DATA                      = 0x65,       ///< Location field pointing to the data portion of PMU firmware
      UCODE_PATCH                   = 0x66,       ///< Microcode patch
      CORE_MCEDATA                  = 0x67,       ///< Core MCE data
      BIOS_APCB_INFO_BACKUP         = 0x68,       ///< Backup Agesa PSP Customization Block (APCB)
      BIOS_DIR_LV2                  = 0x70,       ///< BIOS entry points to Level 2 BIOS DIR
      DISCRETE_USB4_FIRMWARE        = 0x71,       ///< Discrete USB4 Firmware volumes
    };

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

    def __init__(
            self,
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

            unknownTrailingBinary: bytes
    ):
        assert signature == self._signature(), "ZenEfs signature missmatch, expected {}, got {}".format(
            self._signature().hex().upper(), signature.hex().upper()
        )

        # TODO   one problem is    all "references" / offsets here are 32 bit and are hence different to the ones used in directories
        # TODO   maybe create a "EfsReference" class  and make the "ZenReference" into "ZenDirectoryReference"

        self._offset: int = offset

        self._imcFirmware = EfsReference.fromOffset(imcFirmware)
        self._gbeFirmware = EfsReference.fromOffset(gbeFirmware)
        self._xHciFirmware = EfsReference.fromOffset(xHciFirmware)
        self._pspDirectory = EfsReference.fromOffset(pspDirectory)                      # used with Naples and other Zen1(+)

        self._pspOrComboDirectory = EfsReference.fromOffset(pspOrComboDirectory)
        self._biosDirectory0 = EfsReference.fromOffset(biosDirectory0)
        self._biosDirectory1 = EfsReference.fromOffset(biosDirectory1)
        self._biosOrComboDirectory = EfsReference.fromOffset(biosOrComboDirectory)

        self._unknownTrailingBinary = unknownTrailingBinary

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

