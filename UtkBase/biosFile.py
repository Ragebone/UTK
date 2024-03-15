from typing import List

from UtkBase.capsuleHeaders.capsuleHeaderFactory import CapsuleHeaderFactory
from UtkBase.interfaces.capsuleheader import CapsuleHeader
from UtkBase.images.image import Image
from UtkBase.images.imageFactory import ImageFactory
from UtkBase.interfaces.serializable import serializable


class BiosFile(serializable):
    """
    Represents the Motherboards Bios- or rather UEFI-Image -files as they are delivered by the OEM.
    Formats vary with this supporting binary formats like '.bin' and '.rom' as well as '.CAP'.
    The binary contains at least one, lets call it "Firmware" or "UEFI" 'image'.
    Encapsulated *-files like '.CAP' start with a 'capsuleHeader' preceding the 'images'.

    Main entry point for using the framework with a motherboards BiosFile.
    Simply put:
        bios = BiosFile.fromFilepath('Path/to/file')
    :or
        bios = BiosFile.fromBinary(fileHandle.read())

    Serializable; Use bios.serialize() to get the orignial or new / changed binary back.
    """

    @classmethod
    def fromFilepath(cls, filePath: str) -> 'BiosFile':
        """
        Open and build a BiosFile from the given Path.
        Used as the main and easy entry point to the framework.
        Does not catch, handle exceptions yourself!
        :param filePath: FilePath as a string
        :return: BiosFile or Errors
        """

        fileHandle = open(filePath, 'rb')
        BINARY = fileHandle.read()
        fileHandle.close()

        bios = BiosFile.fromBinary(BINARY)
        return bios

    @classmethod
    def fromBinary(cls, binary: bytes, capsuleHeader: CapsuleHeader = None) -> 'BiosFile':
        """
        Build a BiosFile from the given binary.
        Optional CapsuleHeader can be passed in case it was already built previously.
        Does not catch, handle exceptions yourself!

        :param binary: Bytes to build the BiosFile from
        :param capsuleHeader: Optional, previously built CapsuleHeader to not waste that
        :return: BiosFile or Errors
        """
        if capsuleHeader is None:
            capsuleHeader: CapsuleHeader = CapsuleHeaderFactory.fromBinary(binary)

        images: List[Image] = []

        offset: int = 0
        if capsuleHeader is not None:
            offset = capsuleHeader.getSize()

        LENGTH_OF_BINARY = len(binary)
        while offset < LENGTH_OF_BINARY:
            IMAGE_BINARY = binary[offset:]
            image = ImageFactory.fromBinary(IMAGE_BINARY)
            images.append(image)
            offset += image.getSize()

        return cls(capsuleHeader, images)

    def __init__(self, capsuleHeader: CapsuleHeader = None, images: List[Image] = None):
        self._capsuleHeader: CapsuleHeader = capsuleHeader
        self._images: List[Image] = [] if images is None else images

    def getImages(self) -> List[Image]:
        """
        Get a copy of all images contained in the BiosFile.

        :return: Copied List of images
        """
        return self._images.copy()

    def getSize(self) -> int:
        """
        Get the biosFiles Size in bytes.
        Has to be calculated from its content every time in case something changed.

        :return: Size
        """
        size = 0
        if self._capsuleHeader is not None:
            size += self._capsuleHeader.getSize()
        for image in self.getImages():
            size += image.getSize()
        return size

    def toString(self, lineWidth: int = 100) -> str:
        line = u'\u2500' * lineWidth + "\n"
        fileOffset = 0x00
        outString = ""
        if self._capsuleHeader is not None:
            outString += "{:<15} {:<20}\n".format("File offset", "Capsule type")
            outString += "{:<15} {:<20}\n".format(hex(fileOffset), self._capsuleHeader.__class__.__name__)
            outString += self._capsuleHeader.toString()
            outString += line
            fileOffset += self._capsuleHeader.getSize()

        for image in self._images:
            if image is not None:
                outString += "{:<15} {:<20}\n".format("File offset", "Image type")
                outString += "{:<15} {:<20}\n\n".format(hex(fileOffset), image.__class__.__name__)
                outString += image.toString()
                fileOffset += image.getSize()
        return outString

    def serialize(self) -> bytes:
        """ Serializable """
        binary = bytes()

        if self._capsuleHeader is not None:
            binary += self._capsuleHeader.serialize()

        for image in self._images:
            imageBinary = image.serialize()
            binary += imageBinary
        return binary
