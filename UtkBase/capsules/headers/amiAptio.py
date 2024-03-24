import struct
from typing import Any

from UtkBase.capsules.headers.headerInterface import CapsuleHeader
from UtkBase.uefiGuid import UefiGuid


class AmiAptioCapsuleHeader(CapsuleHeader):

    @classmethod
    def _struct(cls) -> struct:
        return struct.Struct('<16sIIIHH')
        # TODO handle RomLayoutOffsets
        # EfiCapsuleHeader
        # RomImageOffset;  // offset in bytes from the beginning of the capsule header to the start of the capsule volume
        # RomLayoutOffset; // offset to the table of the module descriptors in the capsule's volume that are included in the signature calculation

    @classmethod
    def fromBinary(cls, binary: bytes) -> 'AmiAptioCapsuleHeader':
        HEADER_BINARY_VALUES = binary[:cls._struct().size]
        (
            CAPSULE_GUID_BINARY,
            capsuleSize,
            flags,
            capsuleImageSize,
            romImageOffset,
            romLayoutOffset
         ) = cls._struct().unpack(HEADER_BINARY_VALUES)

        capsuleGuid = UefiGuid.fromBinary(CAPSULE_GUID_BINARY)
        TRAILING_CAPSULE_BINARY = binary[cls._struct().size:romImageOffset]
        return cls(capsuleGuid, capsuleSize, flags, capsuleImageSize, romImageOffset, romLayoutOffset, TRAILING_CAPSULE_BINARY)

    def __init__(self, capsuleGuid: UefiGuid, capsuleSize, flags, capsuleImageSize, romImageOffset, romLayoutOffset, trailingCapsuleBinary):
        assert capsuleGuid.toString() in [
            "4A3CA68B-7723-48FB-803D-578CC1FEC44D",
            "14EEBB90-890A-43DB-AED1-5D3C4588A418"
        ], f"Wrong guid for AMI Capsule, got {capsuleGuid.toString()}"

        self._capsuleGuid: UefiGuid = capsuleGuid
        self._capsuleSize: int = capsuleSize
        self._flags: int = flags
        self._capsuleImageSize: int = capsuleImageSize                          # TODO use this value in the image factories
        self._romImageOffset: int = romImageOffset
        self._romLayoutOffset: int = romLayoutOffset

        self._trailingCapsuleBinary: bytes = trailingCapsuleBinary              # What comes after the header-struct till the image

    def getSize(self) -> int:
        return self._struct().size

    def getCapsuleSize(self) -> int:
        # TODO verify that the "header size" matches with the RomImageOffset, otherwise, this is a problem
        return self._capsuleSize

    def getEncapsulatedImageSize(self) -> int:
        return self._capsuleImageSize

    def toDict(self) -> dict[str, Any]:
        return {
            "class": self.__class__.__name__,
            "guid": self._capsuleGuid,
            "capsuleSize": self._capsuleSize,
            "flags": self._flags,
            "capsuleImageSize": self._capsuleImageSize,
            "romImageOffset": self._romImageOffset,
            "romLayoutOffset": self._romLayoutOffset,
            "trailingCapsuleBinary": self._trailingCapsuleBinary
        }

    def toString(self):
        outString = "{:<40} {:<20} {:<20} {:<20} {:<20} {:<20}\n".format(
            "Guid", "CapsuleSize", "flags", "capsuleImageSize", "romImageOffset", "romLayoutOffset"
        )
        outString += "{:<40} {:<20} {:<20} {:<20} {:<20} {:<20}\n".format(
            self._capsuleGuid.toString(), hex(self._capsuleSize), hex(self._flags), hex(self._capsuleImageSize), hex(self._romImageOffset), hex(self._romLayoutOffset)
        )
        return outString

    def serialize(self) -> bytes:
        binary = self._struct().pack(
            self._capsuleGuid.serialize(),
            self._capsuleSize,
            self._flags,
            self._capsuleImageSize,
            self._romImageOffset,
            self._romLayoutOffset
        )
        binary += self._trailingCapsuleBinary
        return binary
