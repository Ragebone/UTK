import textwrap

from UtkBase.capsules.capsule import Capsule
from UtkBase.capsules.headers.factory import CapsuleHeaderFactory
from UtkBase.capsules.headers.header import CapsuleHeader


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

    def toJson(self, depth: int = 0) -> str:
        """

        :param depth: if depth is  smaller than 0, just return your class-name or as minimal info as possible.
        :return: A Json string
        """
        if depth < 0:
            return f'{{"ClassName": "{self.__class__.__name__}"}}'

        jsonString: str = textwrap.dedent(
            f"""
            {{
                "ClassName": "{self.__class__.__name__}",
                "CapsuleHeader": {self._header.toJson(depth - 1)}
            }}       
            """
        )
        return jsonString

    def serialize(self) -> bytes:
        # TODO proper serialization so that modifications can be useful
        return self._binary
