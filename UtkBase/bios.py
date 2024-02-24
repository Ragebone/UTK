from typing import List

from UtkBase.capsuleHeaders.capsuleHeaderFactory import CapsuleHeaderFactory
from UtkBase.interfaces.capsuleheader import CapsuleHeader
from UtkBase.images.image import Image
from UtkBase.images.imageFactory import ImageFactory
from UtkBase.interfaces.serializable import serializable


class Bios(serializable):

    @classmethod
    def fromBinary(cls, binary: bytes, capsuleHeader: CapsuleHeader = None) -> 'Bios':

        if capsuleHeader is None:
            capsuleHeader = CapsuleHeaderFactory.fromBinary(binary)

        if capsuleHeader is not None:
            binary = binary[capsuleHeader.getSize():]

        images: List[Image] = []
        offset = 0
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
        return self._images.copy()

    def getSize(self) -> int:
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
        binary = bytes()

        if self._capsuleHeader is not None:
            binary += self._capsuleHeader.serialize()

        for image in self._images:
            imageBinary = image.serialize()
            binary += imageBinary
        return binary
