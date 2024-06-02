from UtkAmd.uefi.images.zenImage import ZenImage
from UtkAmd.psp.efs.efs import EmbeddedFirmwareStructure
from UtkAmd.psp.efs.efsFactory import EfsFactory
from UtkBase.images.genericImage import GenericImage
from UtkBase.images.image import Image
from UtkBase.images.imageElement import ImageElement
from UtkBase.images.paddings.paddingFactory import PaddingFactory
from UtkBase.images.volumes.volumeFactory import VolumeFactory


VOLUME_START_TO_SIGNATURE_OFFSET = 40


class ImageFactory:

    @staticmethod
    def fromBinary(binary: bytes, imageOffset: int = 0) -> Image:
        """
        Constructs an image from the given binary by making a list of the images content.
        The List is made by searching for volumes first and filling the gaps with padding objects.

        Is supposed to decide on whether it is a generic, AMD or intel based image

        :param binary: Bytes to construct the image from.
        :param imageOffset: Optional informative offset where the Image is located inside the parent.
        :return: GenericImage; TODO implement more variants
        """
        imageElements: list[ImageElement] = []

        # look for specific OEM image types

        # AMD Ryzen
        try:
            return ImageFactory.attemptBuildingAmdZenImage(binary, imageOffset)
        except Exception as ex:
            from UtkBase.biosFile import BiosFile
            if BiosFile.dontHandleExceptions:
                raise ex
            # TODO error / issue reporting?

        IMAGE_LENGTH = len(binary)
        offset = 0
        while offset < IMAGE_LENGTH:
            NEXT_VOLUME_OFFSET = binary.find(b'_FVH', offset) - VOLUME_START_TO_SIGNATURE_OFFSET

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

        genericImage = GenericImage.fromImageElements(imageElements, imageOffset)
        return genericImage

    @staticmethod
    def attemptBuildingAmdZenImage(binary: bytes, imageOffset: int = 0) -> ZenImage:
        """
        Asserts if the binary is not an AMD Zen compatible image.
        Otherwise, search for further images to limit construction to only the first found image.

        :param binary: Image binary to check and construct from
        :param imageOffset: Optional offset of where the image is located at inside the Bios-File
        :return: First found and constructed ZenImage for Zen
        """
        embeddedFirmwareStructure = ImageFactory.getAmdFirmwareStructures(binary)

        assert embeddedFirmwareStructure is not None, "AMD Image must have an Embedded Firmware Structure (EFS)"

        additionalEfs = ImageFactory.getAmdFirmwareStructures(binary, 0x1000000)
        if additionalEfs is not None:
            # 16MB stacked images
            # Limit this image's binary to the 16MB it should be
            binary = binary[:0x1000000]

        amdUefiImage = ZenImage.fromBinary(binary, embeddedFirmwareStructure, imageOffset)
        return amdUefiImage

    @staticmethod
    def getAmdFirmwareStructures(binary: bytes, findOffset: int = 0) -> EmbeddedFirmwareStructure:
        """
        Get AMD Zen based Embedded Firmware Structure.
        Probes fixed offsets on which an EFS is expected.

        :param binary: The Image binary to search through
        :param findOffset: Offset to start searching from
        :return: Found and constructed EFS
        """
        for offset in ZenImage.EFS_OFFSETS:
            offset += findOffset
            potentialEfsSignature = binary[offset:offset + 4]
            if potentialEfsSignature != b'\xAA\x55\xAA\x55':
                continue

            EFS_BINARY = binary[offset:]
            embeddedFirmwareStructure = EfsFactory.fromBinary(EFS_BINARY, offset - findOffset)
            return embeddedFirmwareStructure
