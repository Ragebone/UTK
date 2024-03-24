from UtkBase.images.volumes.headers.volumeHeader import VolumeHeader
from UtkBase.images.volumes.volume import Volume


class VolumeFactory:

    @staticmethod
    def fromBinary(binary: bytes, offset: int = None) -> Volume:
        """

        :param binary:
        :param offset:
        :return:
        """
        header = VolumeHeader.fromBinary(binary)
        assert header is not None, "Failed building VolumeHeader at offset {} from {]".format(
            hex(offset), binary[:0xFF].upper().hex()
        )

        volume = Volume.fromBinary(binary, header, offset)
        return volume
