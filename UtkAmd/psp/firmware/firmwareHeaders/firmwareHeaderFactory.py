import struct

from UtkAmd.psp.firmware.firmwareHeaders.pspFirmwareHeader import PspFirmwareHeader


class FirmwareHeaderFactory:

    @staticmethod
    def fromBinary(binary: bytes):
        if len(binary) < 0x100:
            # TODO investigate why this would be called with just 16 bytes
            # NOTE ANSWER wrappedIKEKS
            return None

        # Magic might also just be a weird version-number
        zeroes, magic = struct.unpack("<16s 4s", binary[:20])     # Zeros - Magic, signedSize, encrypted

        if zeroes != 16 * b'\x00':
            return None

        if magic == b'PSP':
            return PspFirmwareHeader.fromBinary(binary)

        if magic == b'\x05\x00\x00\x00':
            return PspFirmwareHeader.fromBinary(binary)

        # TODO there is something like a "legacy Header"

        return None
