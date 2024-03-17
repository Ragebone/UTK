import struct
import textwrap

from UtkBase.uefiGuid import UefiGuid


class ToshibaCapsuleHeader:
    """
    A Toshiba capsule header implementation
    TODO add reference to the UEFITool or other references
    """
    @classmethod
    def _struct(cls) -> struct:
        return struct.Struct('<16sIII')     # CapsuleGuid HeaderSize FullSize flags

    @classmethod
    def fromBinary(cls, binary: bytes) -> 'ToshibaCapsuleHeader':
        GUID_BINARY, headerSize, capsuleSize, flags = cls._struct().unpack(binary[:cls._struct().size])
        guid = UefiGuid.fromBinary(GUID_BINARY)

        return cls(guid, headerSize, capsuleSize, flags)

    def __init__(self, guid: UefiGuid, headerSize: int, fullSize: int, flags: int):
        assert guid.toString() in [
            "539182B9-ABB5-4391-B69A-E3A943F72FCC"
        ], f"Wrong guid for ToshibaCapsuleHeader, got {guid.toString()}"

        self._capsuleGuid = guid
        self._capsuleSize = headerSize
        self._fullSize = fullSize
        self._flags = flags

    def getSize(self) -> int:
        return self._struct().size

    def getCapsuleSize(self) -> int:
        # TODO verify that the "header size" matches with the RomImageOffset, otherwise, this is a problem
        return self._capsuleSize

    def getEncapsulatedImageSize(self) -> int:
        return self._fullSize

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
                   "GUID": "{self._capsuleGuid.toString()}",
                   "CapsuleSize": "{hex(self._capsuleSize)}",
                   "Flags": "{hex(self._flags)}",
                   "CapsuleImageSize": "{hex(self._fullSize)}"
               }}       
               """
        )
        return jsonString

    def serialize(self):
        binary = self._struct().pack(self._capsuleGuid.serialize(), self._capsuleSize, self._fullSize, self._flags)
        return binary
