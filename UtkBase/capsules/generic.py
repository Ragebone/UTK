from typing import Any

from UtkBase.capsules.capsule import Capsule
from UtkBase.capsules.headers.factory import CapsuleHeaderFactory
from UtkBase.capsules.headers.headerInterface import CapsuleHeader


class GenericCapsule(Capsule):
    @classmethod
    def fromBinary(cls, binary, header: CapsuleHeader = None) -> 'Capsule':

        if header is None:
            header: CapsuleHeader = CapsuleHeaderFactory.fromBinary(binary)

        CAPSULE_SIZE = header.getCapsuleSize()
        binary = binary[:CAPSULE_SIZE]                  # Self limit

        capsule = cls(header, binary)
        return capsule

    def __init__(self, capsuleHeader: CapsuleHeader, binary: bytes):
        self._header = capsuleHeader
        self._binary = binary

    def getSize(self) -> int:
        return self._header.getCapsuleSize()

    def getImageSize(self) -> int:
        return self._header.getEncapsulatedImageSize()

    def toDict(self) -> dict[str, Any]:
        return {
            "class": self.__class__.__name__,
            "capsuleHeader": self._header,
            "binary": self._binary
        }

    def serialize(self) -> bytes:
        # TODO proper serialization so that modifications can be useful
        return self._binary
