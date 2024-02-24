from UtkBase.images.imageElement import ImageElement
from UtkBase.images.volumes.headers.externalVolumeHeader import ExternalVolumeHeader
from UtkBase.images.volumes.headers.volumeHeader import VolumeHeader


class Volume(ImageElement):

    @classmethod
    def fromBinary(cls, binary: bytes, volumeOffset: int, header: VolumeHeader = None) -> 'Volume':
        """

        :param binary: Possibly unlimited binary containing more than just the volume
        :param volumeOffset: Offset the volume is located at in the image
        :param header:
        :return:
        """
        if header is None:
            header = VolumeHeader.fromBinary(binary)

        assert header is not None, "None VolumeHeader from offset: {}, binary: {}".format(
            hex(volumeOffset), binary[:256]
        )

        VOLUME_BINARY = binary[:header.getVolumeSize()]
        EXTERNAL_HEADER_OFFSET = header.getExternalHeaderOffset()

        BINARY_BETWEEN_HEADERS = VOLUME_BINARY[header.getSize():EXTERNAL_HEADER_OFFSET]

        externalHeader = ExternalVolumeHeader.fromBinary(VOLUME_BINARY[EXTERNAL_HEADER_OFFSET:])

        CONTENT_START_OFFSET = EXTERNAL_HEADER_OFFSET + externalHeader.getSize()
        CONTENT_BINARY = VOLUME_BINARY[CONTENT_START_OFFSET:]
        # TODO use the guid of the external header to decide what is going on here.

        volume = cls(volumeOffset, header, BINARY_BETWEEN_HEADERS, externalHeader, CONTENT_BINARY)

        return volume

    def __init__(self, offset: int, header: VolumeHeader, binaryBetweenHeaders, externalHeader: ExternalVolumeHeader, contentBinary: bytes):
        self._offset: int = offset
        self._header: VolumeHeader = header
        self._binaryBetweenHeaders: bytes = binaryBetweenHeaders
        self._externalHeader: ExternalVolumeHeader = externalHeader
        self._contentBinary: bytes = contentBinary

    def getOffset(self) -> int:
        return self._offset

    def getSize(self) -> int:
        return self._header.getVolumeSize()

    def toString(self, lineWidth: int = 100) -> str:
        line = u'\u2500' * lineWidth + "\n"
        outString = ""

        if self._header is not None:
            outString += self._header.toString()
            outString += line

        if self._externalHeader is not None:
            outString += self._externalHeader.toString()
            outString += line

        return outString

    def serialize(self):
        outputBinary = self._header.serialize()
        outputBinary += self._binaryBetweenHeaders
        outputBinary += self._externalHeader.serialize()
        outputBinary += self._contentBinary
        return outputBinary
