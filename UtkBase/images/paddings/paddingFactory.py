from UtkBase.images.imageElement import ImageElement
from UtkBase.images.paddings.emptyPadding import EmptyPadding
from UtkBase.images.paddings.padding import Padding
from UtkBase.utility import binaryIsEmpty


class PaddingFactory:
    @staticmethod
    def fromBinary(binary: bytes, offset: int = None) -> ImageElement:
        """
        Construct the correct padding from the given binary
        If binary consists only of 0xFF, it will be an EmptyPadding object

        :param binary: Bytes to construct the padding from
        :param offset: Place in the image that the padding is located at. TODO can this really be none?
        :return: Constructed Padding,  either EmptyPadding or just a Padding.
        """
        if binaryIsEmpty(binary):
            return EmptyPadding.fromBinary(binary, offset)

        return Padding.fromBinary(binary, offset)
