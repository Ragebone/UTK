from typing import List, Any

from UtkBase.images.imageElement import ImageElement
from UtkBase.images.image import Image


class GenericImage(Image):
    """
    A generic UEFI image implementation assuming that an image is just UEFI Volumes and possibly paddings inbetween.
    Hence, this features just a List of 'ImageElement's those being UEFI Volumes and Padding objects.
    This does not feature any understanding or capability for any OEM.

    Useful as a reference and fallback in case something goes wrong with an OEM image.
    Or for general testing and getting something up and running quickly, like this project here.

    AMD based images are a bit more complex with the PSP firmware structures.
    Intel based images similarly so.
    """

    @classmethod
    def fromImageElements(cls, contents: List[ImageElement], imageOffset: int = 0) -> Image:
        """
        Construct a generic image from a list of UEFI based ImageElements
        :param contents: List of UEFI volumes, paddings, those are ImageElements
        :param imageOffset: Optional informative offset for where the Image is inside the parent
        :return: An GenericImage object
        """
        return cls(contents, imageOffset)

    @classmethod
    def fromDict(cls, dictionary: dict) -> 'GenericImage':
        return cls(dictionary.get('content', []))

    def __init__(self, contents=None, imageOffset: int = 0):

        # Informational offset
        self._offset = imageOffset
        # TODO consider making this a dictionary with the key being the offset inside the image
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

    def toDict(self) -> dict[str, Any]:
        return {
            "class": self.__class__.__name__,
            "offset": self._offset,
            "content": self._contents
        }

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
        """ Serializable """
        imageBinary = bytes()
        for imageElement in self._contents:
            BINARY = imageElement.serialize()
            imageBinary += BINARY
        return imageBinary
