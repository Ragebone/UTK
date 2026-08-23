import struct

from UtkAmd.psp.directories.directoryEntries.entryReference import EntryReference
from UtkAmd.psp.zenGenerations import ZenGeneration
from UtkAmd.psp.zenReference import ZenReference
from UtkAmd.utkAmdInterfaces import UtkAMD
from UtkCommon.interfaces.reference import Reference
from UtkCommon.interfaces.serializable import Serializable


class A_B_Header(Serializable, UtkAMD):
    @classmethod
    def _struct(cls) -> struct.Struct:
        """
        16 unknown bytes
        Offset
        1 unknown byte
        3 ZenGenerationID
        8 unknown bytes
        :return:
        """
        return struct.Struct('<16s I 1s 3s 8s')

    @classmethod
    def fromBinary(cls, binary: bytes, offset: int = None) -> 'Directory':
        assert binary is not None, "Binary is None"

        body = binary[:32]
        assert len(body) == 32, "To few bytes for A B Header | IHS structure"

        unknown1, offset, unknown2, zenGenerationId, unknown3 = cls._struct().unpack(body)
        reference = EntryReference.fromOffset(offset)
        zenGeneration = ZenGeneration(zenGenerationId)
        return cls(body, unknown1,  reference, unknown2, zenGeneration, unknown3)

    def __init__(self, body, unknown1, directoryReference, unknown2, zenGeneration, unknown3):
        self._body = body
        self._unknown1 = unknown1
        self._directoryReference: ZenReference = directoryReference
        self._unknown2 = unknown2
        self._zenGeneration: ZenGeneration = zenGeneration
        self._unknown3 = unknown3

        self._references = []

    def getDirectoryReference(self) -> 'ZenReference':
        return self._directoryReference

    def registerReference(self, reference: Reference) -> None:
        self._references.append(reference)

    def getReferences(self) -> list[Reference]:
        return self._references

    def getSize(self) -> int:
        return 32

    def serialize(self) -> bytes:
        output = self._struct().pack(
            self._unknown1,
            self._directoryReference.getOffset(),
            self._unknown2,
            self._zenGeneration.value,
            self._unknown3
        )
        return output