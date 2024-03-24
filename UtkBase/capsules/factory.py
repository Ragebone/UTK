from UtkBase.capsules.capsule import Capsule
from UtkBase.capsules.generic import GenericCapsule
from UtkBase.capsules.headers.factory import CapsuleHeaderFactory
from UtkBase.capsules.headers.headerInterface import CapsuleHeader


class CapsuleFactory:
    """
    Factory for constructing a capsule.
    Which capsule is up to the factory and depends on the input
    Has the responsibility to decide which capsule to construct.
    """

    @staticmethod
    def fromBinary(binary: bytes, offset: int = 0) -> Capsule:
        """
        Construct a Capsule from the given binary.

        Returns None of there is nothing identifiable as a capsule

        :param binary: Bytes to construct the capsule from
        :param offset: Optional informative location inside the parent; usually a BiosFile.
        Defaults to 0. Can be None.
        :return: Capsule or None if no capsule can be identified.
        """

        header: CapsuleHeader = CapsuleHeaderFactory.fromBinary(binary)
        if header is None:
            return None

        return GenericCapsule.fromBinary(binary, header, offset)

    # TODO add fromDirectory() for importing previously extracted BiosFiles
