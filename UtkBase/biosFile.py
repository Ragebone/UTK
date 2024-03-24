from typing import List, Any

from UtkBase.capsules.capsule import Capsule
from UtkBase.capsules.factory import CapsuleFactory
from UtkBase.images.image import Image
from UtkBase.images.imageFactory import ImageFactory
from interfaces import Serializable


class BiosFile(Serializable):
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

    Serializable; Use bios.serialize() to get the original or new / changed binary back.
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
    def fromBinary(cls, binary: bytes, capsule: Capsule = None, fileOffset: int = 0) -> 'BiosFile':
        """
        Build a BiosFile from the given binary.
        Optional CapsuleHeader can be passed in case it was already built previously.
        Does not catch, handle exceptions yourself!

        :param binary: Bytes to build the BiosFile from
        :param capsule: Optional, previously built Capsule to not waste that
        :param fileOffset: Optional int offset where the BiosFile is located at inside the binary.
        Defaults to 0 since the "BiosFile" is the file.
        :return: BiosFile or Errors
        """

        if capsule is None:
            capsule: Capsule = CapsuleFactory.fromBinary(binary, fileOffset)

        images: List[Image] = []

        imageOffset = 0
        if capsule is not None:
            imageOffset = capsule.getSize()

        LENGTH_OF_BINARY = len(binary)
        while imageOffset < LENGTH_OF_BINARY:
            IMAGE_BINARY = binary[imageOffset:]
            image = ImageFactory.fromBinary(IMAGE_BINARY, imageOffset)
            images.append(image)
            imageOffset += image.getSize()

        return cls(capsule, images, fileOffset)

    def __init__(self, capsule: Capsule = None, images: List[Image] = None, offset: int = 0):

        # informative offset
        self._offset: int = offset
        self._capsule: Capsule = capsule
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
        if self._capsule is not None:
            size += self._capsule.getSize()
        for image in self.getImages():
            size += image.getSize()
        return size

    def toDict(self) -> dict[str, Any]:
        return {
            "class": self.__class__.__name__,
            "offset": self._offset,
            "capsule": self._capsule,
            "images": self._images
        }

    def toString(self, lineWidth: int = 100) -> str:
        line = u'\u2500' * lineWidth + "\n"
        fileOffset = 0x00
        outString = ""
        if self._capsule is not None:
            outString += "{:<15} {:<20}\n".format("File offset", "Capsule type")
            outString += "{:<15} {:<20}\n".format(hex(fileOffset), self._capsule.__class__.__name__)
            outString += self._capsule.toString()
            outString += line
            fileOffset += self._capsule.getSize()

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

        if self._capsule is not None:
            binary += self._capsule.serialize()

        for image in self._images:
            imageBinary = image.serialize()
            binary += imageBinary
        return binary
