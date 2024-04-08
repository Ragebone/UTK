import logging
from typing import Any

from UtkBase.images.imageElement import ImageElement
from UtkBase.images.volumes.files.file import File
from UtkBase.images.volumes.headers.externalVolumeHeader import ExternalVolumeHeader
from UtkBase.images.volumes.headers.volumeHeader import VolumeHeader
from UtkBase.utility import alignOffset, binaryIsEmpty, fillBinaryTill


FILE_ALIGNMENT = 0x08


class Volume(ImageElement):
    """
    UEFI volume implementation.

    Volumes have a clear header with the easily identifiable magic '_FVH'.
    Can contain additional headers or so called header-extensions.

    And then contain "Files" inside a "FileSystem"
    """

    @classmethod
    def fromBinary(cls, binary: bytes, header: VolumeHeader = None, volumeOffset: int = 0) -> 'Volume':
        """

        :param binary: Possibly unlimited binary containing more than just the volume
        :param header: Optional previously parsed VolumeHeader
        :param volumeOffset: Optional informative offset the volume is located at in the image
        :return:
        """
        if header is None:
            header = VolumeHeader.fromBinary(binary)

        assert header is not None, "No volumeHeader from offset: {}, binary: {}".format(
            hex(volumeOffset), binary[:256]
        )
        # TODO use the guid of the external header to decide what is going on here.
        # TODO maybe move this into the volume factory or something.

        VOLUME_SIZE = header.getVolumeSize()
        VOLUME_BINARY = binary[:VOLUME_SIZE]

        HEADER_SIZE = header.getSize()
        EXTERNAL_HEADER_OFFSET = header.getExternalHeaderOffset()

        binaryBetweenHeaders = VOLUME_BINARY[HEADER_SIZE:EXTERNAL_HEADER_OFFSET]

        externalHeader = ExternalVolumeHeader.fromBinary(VOLUME_BINARY[EXTERNAL_HEADER_OFFSET:])

        EXTERNAL_HEADER_SIZE = externalHeader.getSize()
        CONTENT_START_OFFSET = EXTERNAL_HEADER_OFFSET + EXTERNAL_HEADER_SIZE

        files: dict[str, File] = {}

        # Local import because Sections in a File can contain Volumes, circular import otherwise.
        from UtkBase.images.volumes.files.fileFactory import FileFactory

        offset = CONTENT_START_OFFSET
        while offset < VOLUME_SIZE:
            fileBinary = VOLUME_BINARY[offset:]
            file = FileFactory.fromBinary(fileBinary, offset)

            if file is None:
                break

            files[hex(offset)] = file

            FILE_SIZE = file.getSize()
            ALIGNED_FILE_SIZE = alignOffset(FILE_SIZE, FILE_ALIGNMENT)
            offset += ALIGNED_FILE_SIZE

            if ALIGNED_FILE_SIZE > FILE_SIZE:
                PADDING_BINARY: bytes = fileBinary[FILE_SIZE:ALIGNED_FILE_SIZE]
                if not binaryIsEmpty(PADDING_BINARY):
                    logging.error("Padding between files is {} instead of 0xFFs and will be DISCARDED!".format(PADDING_BINARY.hex().upper()))
        else:
            pass
            # This should be the case when the loop above has reached a "Volume free Space"
            # At the end of the volume, filled just with FFs

        volume = cls(header, binaryBetweenHeaders, externalHeader, files, volumeOffset)

        return volume

    def __init__(self, header: VolumeHeader, binaryBetweenHeaders: bytes, externalHeader: ExternalVolumeHeader, files: dict[str, File], offset: int = 0):

        # informational offset
        self._offset: int = offset
        self._header: VolumeHeader = header
        self._binaryBetweenHeaders: bytes = binaryBetweenHeaders
        self._externalHeader: ExternalVolumeHeader = externalHeader
        self._files: dict[str, File] = files                            # Key: Hex(Absolute offset from the start of the volume)

    def getOffset(self) -> int:
        return self._offset

    def getSize(self) -> int:
        return self._header.getVolumeSize()

    def getSortedFileKeys(self) -> list:
        return sorted(self._files, key=lambda key: int(key, 16))

    def getSortedFiles(self) -> list[tuple[str, File]]:
        return sorted(self._files.items(), key=lambda item: int(item[0], 16))

    def toDict(self) -> dict[str, Any]:
        return {
            "offset": self._offset,
            "headers": self._header,
            "binaryBetweenHeaders": self._binaryBetweenHeaders,
            "externalHeader": self._externalHeader,
            "files": self._files
        }

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

    def serialize(self) -> bytes:
        outputBinary = self._header.serialize()
        outputBinary += self._binaryBetweenHeaders
        outputBinary += self._externalHeader.serialize()

        sortedFileKeys = self.getSortedFileKeys()
        for key in sortedFileKeys:
            currentOffset = len(outputBinary)
            fileOffset = int(key, 16)
            file = self._files.get(key)

            assert currentOffset <= fileOffset, "Volume content overflow for offset {} with fileOffset {}".format(hex(currentOffset), hex(fileOffset))

            # Paddings between files
            outputBinary = fillBinaryTill(outputBinary, fileOffset)

            fileBinary = file.serialize()
            EXPECTED_FILE_SIZE = file.getSize()
            BINARY_SIZE = len(fileBinary)
            assert BINARY_SIZE == EXPECTED_FILE_SIZE, "File size missmatch for offset {} with size {}, expected {}".format(hex(fileOffset), hex(BINARY_SIZE), hex(EXPECTED_FILE_SIZE))
            outputBinary += fileBinary

        # Volume Free Space handling
        outputBinary = fillBinaryTill(outputBinary, self.getSize())
        return outputBinary
