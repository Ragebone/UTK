

from UtkBase.capsules.generic import GenericCapsule
from UtkBase.capsules.headers.factory import CapsuleHeaderFactory
from UtkBase.capsules.headers.header import CapsuleHeader


class CapsuleFactory:
    @staticmethod
    def fromBinary(binary: bytes):

        header: CapsuleHeader = CapsuleHeaderFactory.fromBinary(binary)
        if header is None:
            return None

        return GenericCapsule.fromBinary(binary, header)
