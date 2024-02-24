from typing import List

from UtkBase.images.imageElement import ImageElement
from UtkBase.images.image import Image


class GenericImage(Image):

    @classmethod
    def fromImageElements(cls, contents: List[ImageElement]) -> Image:
        """
        Construct a generic image from a list of UEFI based ImageElements
        :param contents: List of UEFI volumes, paddings, those are ImageElements
        :return: An GenericImage object
        """
        return cls(contents)

    def __init__(self, contents=None):
        self._contents: List[ImageElement] = [] if contents is None else contents

    def getSize(self):
        """
        Get the current size of the image.
        To handle changes of the image contents, this gets calculated every time

        :return: Int size of the image
        """
        size = 0
        for imageElement in self._contents:
            if imageElement is not None:
                size += imageElement.getSize()
        return size

    def toString(self) -> str:
        imageOffset = 0x00
        outString = ""
        for imageElement in self._contents:
            outString += "{:<15} {:<20}\n".format("Image offset", "Type")
            outString += "{:<15} {:<20}\n".format(hex(imageOffset), imageElement.__class__.__name__)

            outString += imageElement.toString()
            imageOffset += imageElement.getSize()
            outString += "\n"
        return outString

    def serialize(self) -> bytes:
        imageBinary = bytes()
        for imageElement in self._contents:
            BINARY = imageElement.serialize()
            imageBinary += BINARY
        return imageBinary
