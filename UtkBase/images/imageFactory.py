from typing import List

from UtkBase.images.genericImage import GenericImage
from UtkBase.images.image import Image
from UtkBase.images.imageElement import ImageElement
from UtkBase.images.paddings.paddingFactory import PaddingFactory
from UtkBase.images.volumes.volumeFactory import VolumeFactory


class ImageFactory:

    @staticmethod
    def fromBinary(binary: bytes) -> Image:
        """
        Constructs an image from the given binary by making a list of the images content.
        The List is made by searching for volumes first and filling the gaps with padding objects.

        Is supposed to decide on whether it is a generic, AMD or intel based image

        :param binary: Bytes to construct the image from
        :return: GenericImage; TODO implement more variants
        """
        imageElements: List[ImageElement] = []

        IMAGE_LENGTH = len(binary)
        offset = 0
        while offset < IMAGE_LENGTH:
            NEXT_VOLUME_OFFSET = binary.find(b'_FVH', offset) - 40

            if NEXT_VOLUME_OFFSET < 0:
                # No, or last volume in image trailed by padding
                TRAILING_BINARY = binary[offset:]
                padding = PaddingFactory.fromBinary(TRAILING_BINARY, offset)
                imageElements.append(padding)
                break

            if NEXT_VOLUME_OFFSET > offset:
                # Padding between volumes
                PADDING_BINARY = binary[offset:NEXT_VOLUME_OFFSET]
                padding = PaddingFactory.fromBinary(PADDING_BINARY, offset)
                imageElements.append(padding)

            # make a volume
            offset = NEXT_VOLUME_OFFSET
            VOLUME_BINARY = binary[offset:]                         # Unlimited binary, the volume has to limit itself!

            volume = VolumeFactory.fromBinary(VOLUME_BINARY, offset)

            imageElements.append(volume)
            offset += volume.getSize()

        # TODO more then GenericImages
        uefiImage = GenericImage.fromImageElements(imageElements)

        return uefiImage
