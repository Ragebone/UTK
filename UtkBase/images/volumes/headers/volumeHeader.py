import logging
import struct

from UtkBase.images.volumes.headers.blockMap import Block
from UtkBase.uefiGuid import UefiGuid


class VolumeHeader:

    @classmethod
    def _struct(cls) -> struct:
        return struct.Struct('<16s 16s q 4s I H H H B B')

    @classmethod
    def fromBinary(cls, binary: bytes) -> 'VolumeHeader':
        STRUCT_BINARY = binary[:cls._struct().size]
        (
            ZERO_VECTOR,                # fixed
            GUID_BINARY,
            volumeSize,
            magic,                      # fixed
            attributeMask,
            headerSize,
            checksum,
            externalHeaderOffset,
            reserved,
            revision
        ) = cls._struct().unpack(STRUCT_BINARY)

        assert ZERO_VECTOR == b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00', "Reserved must be 16 Bytes of 0s, got {}".format(ZERO_VECTOR.hex().upper())
        assert magic == b'_FVH', "Must have _FVH as magic, got {}".format(magic)

        # limit header binary to its structure and blockMap
        HEADER_BINARY = binary[:headerSize]

        guid = UefiGuid.fromBinary(GUID_BINARY)

        BLOCK_MAP_BINARY = HEADER_BINARY[cls._struct().size:]

        header = cls(guid, volumeSize, attributeMask, headerSize, checksum, externalHeaderOffset,
                     reserved, revision, BLOCK_MAP_BINARY)
        return header

    def __init__(self, guid: UefiGuid, volumeSize, attributeMask, headerSize, checksum, externalHeaderOffset, reserved, revision, blockMapBinary):
        self._guid: UefiGuid = guid
        self._volumeSize = volumeSize
        self._attributeMask = attributeMask
        self._headerSize = headerSize                                   # Includes the BlockMap
        self._checksum = checksum
        self._externalHeaderOffset = externalHeaderOffset
        self._reserved = reserved
        self._revision = revision

        self._blockMapBinary = blockMapBinary

    def getGuid(self) -> UefiGuid:
        return self._guid

    def getSize(self) -> int:
        return self._headerSize

    def getVolumeSize(self) -> int:
        return self._volumeSize

    def getExternalHeaderOffset(self) -> int:
        return self._externalHeaderOffset

    def toString(self) -> str:
        outputString = "{:<40} {:<15} {:<10} {:<15} {:<15} {:<15}\n".format(
            "Guid", "Volume Size", "Magic", "Attribute Mask", "Checksum", "Revision")
        outputString += "{:<40} {:<15} {:<10} {:<15} {:<15} {:<15}\n".format(
            self._guid.toString(), hex(self._volumeSize), "_FVH", self._attributeMask, hex(self._checksum), self._revision)

        return outputString

    def serialize(self) -> bytes:
        ZERO_VECTOR = b'\x00' * 16
        outBinary = self._struct().pack(
            ZERO_VECTOR,
            self._guid.serialize(),
            self._volumeSize,
            b'_FVH',                            # Magic
            self._attributeMask,
            self._headerSize,
            self._checksum,
            self._externalHeaderOffset,
            self._reserved,
            self._revision
        )
        outBinary += self._blockMapBinary
        return outBinary
