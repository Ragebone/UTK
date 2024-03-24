from UtkBase.capsules.capsule import Capsule
from UtkBase.capsules.generic import GenericCapsule
from UtkBase.capsules.headers.factory import CapsuleHeaderFactory
from UtkBase.capsules.headers.headerInterface import CapsuleHeader


class CapsuleFactory:
    @staticmethod
    def fromBinary(binary: bytes) -> Capsule:

        header: CapsuleHeader = CapsuleHeaderFactory.fromBinary(binary)
        if header is None:
            return None

        return GenericCapsule.fromBinary(binary, header)
