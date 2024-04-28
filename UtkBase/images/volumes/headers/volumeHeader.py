import struct

from UtkBase.uefiGuid import UefiGuid
from UtkBase.utility import calculateChecksum16
from utkInterfaces import Header


class VolumeHeader(Header):
    """
    Represents the header at the start of a UEFI Volume.
    The header consists of a structure and the so called Block-Map.
    A checksum only verifies this header.

    It can be easily identified in binary by the 16 leading 0es (Zero Vector) and
    a *Magic* value of '_FVH' following a bit later.
    """

    @classmethod
    def _struct(cls) -> struct:
        """
        https://github.com/LongSoft/UEFITool/blob/c5508535c135612dc921ae0d38eb0cfaae2d33d4/common/ffs.h#L111
        // Volume header
        typedef struct EFI_FIRMWARE_VOLUME_HEADER_ {
            UINT8    ZeroVector[16];
            EFI_GUID FileSystemGuid;
            UINT64   FvLength;
            UINT32   Signature;
            UINT32   Attributes;
            UINT16   HeaderLength;
            UINT16   Checksum;
            UINT16   ExtHeaderOffset;  //Reserved in Revision 1
            UINT8    Reserved;
            UINT8    Revision;
            //EFI_FV_BLOCK_MAP_ENTRY FvBlockMap[2];
        } EFI_FIRMWARE_VOLUME_HEADER;
        """
        # TODO handle version 1 as is stated above
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

        assert ZERO_VECTOR == b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00', f"""
        Reserved must be 16 Bytes of 0s, got {ZERO_VECTOR.hex().upper()}
        """

        assert magic == b'_FVH', "Volume header must have '_FVH' as magic, got {}".format(magic)

        # limit header binary to its structure and blockMap
        HEADER_BINARY = binary[:headerSize]

        guid = UefiGuid.fromBinary(GUID_BINARY)

        BLOCK_MAP_BINARY = HEADER_BINARY[cls._struct().size:]

        header = cls(
            guid,
            volumeSize,
            attributeMask,
            headerSize,
            checksum,
            externalHeaderOffset,
            reserved,
            revision,
            BLOCK_MAP_BINARY
        )

        return header

    def __init__(self, guid: UefiGuid, volumeSize, attributeMask, headerSize, checksum, externalHeaderOffset, reserved, revision, blockMapBinary):
        self._guid: UefiGuid = guid
        self._volumeSize = volumeSize
        self._attributeMask = attributeMask
        self._headerSize = headerSize                                   # Includes the BlockMap
        self._checksum = 0                                              # validates only this header, not the volume. Includes blockMap and zero vector
        self._externalHeaderOffset = externalHeaderOffset
        self._reserved = reserved
        self._revision = revision                                       # TODO check for the Revision, maybe even in the factory

        # TODO add blockMap parsing
        self._blockMapBinary = blockMapBinary

        # validate correctness
        self._checksum = self.validate(checksum)

    def validate(self, CHECKSUM: int = None, updateCheckSum: bool = False) -> bool:
        """
        # TODO really start using this and stuff, this might suck as it is right now
        Validate the header by recalculating and comparing checksums

        :param: CHECKSUM the parsed checksum to validate and reference, None if ignored
        :return: the calculated checksum
        """
        self._checksum = 0
        CURRENT_CHECKSUM = calculateChecksum16(self.serialize())

        if CHECKSUM is not None:
            assert CHECKSUM == CURRENT_CHECKSUM, "Checksums do not match, current {}, expected {]".format(CURRENT_CHECKSUM, CHECKSUM)

        if updateCheckSum:
            self._checksum = CURRENT_CHECKSUM

        return CURRENT_CHECKSUM

    def getGuid(self) -> UefiGuid:
        """Get the UEFI GUID object of the header"""
        return self._guid

    def getSize(self) -> int:
        """Size of this header including blockMap and zero-vector"""
        return self._headerSize

    def getVolumeSize(self) -> int:
        """Size of the UEFI volume, header included"""
        return self._volumeSize

    def getExternalHeaderOffset(self) -> int:
        """Offset the External Header Structure is located at"""
        return self._externalHeaderOffset

    def toDict(self) -> dict[str, any]:
        return {
            "guid": self._guid,
            "volumeSize": self._volumeSize,
            "attributeMask": self._attributeMask,
            "headerSize": self._headerSize,
            "checksum": self._checksum,
            "externalHeaderOffset": self._externalHeaderOffset,
            "reserved": self._reserved,
            "revision": self._revision,
            "blockMapBinary": self._blockMapBinary
        }

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
