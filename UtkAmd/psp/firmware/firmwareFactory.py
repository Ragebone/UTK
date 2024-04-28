import traceback

from UtkAmd.psp.firmware.firmwareBlob import FirmwareBlob
from UtkBase.images.imageElement import ImageElement

FIRMWARE_TYPE_MAPPING = {

}


class FirmwareFactory:
    """
    Factory for AMD PSP specific firmware

    Primary part of all decisions is the firmwareType vale in typed-directorEntries.
    TODO implement handling of specific firmware like the APOB, APCB and others
    """

    @staticmethod
    def fromBinary(firmwareType: int, binary: bytes, offset: int) -> ImageElement:
        """
        Construct some AMD PSP specific firmware from the given binary

        :param firmwareType: Type value from the TypedDirectoryEntry
        :param binary: Binary to build the firmware from
        :param offset: Offset the firmware is located at in the image
        :return: firmware as an ImageElement
        """
        # TODO this could take a typedDirectoryEntry instead of just the instance number

        assert firmwareType is not None, "FirmwareType must not be None"
        assert binary is not None, "Binary must not be None"

        firmwareClass: type[FirmwareBlob] = FIRMWARE_TYPE_MAPPING.get(firmwareType)
        if firmwareClass is None:
            firmware = FirmwareBlob.fromBinary(binary, None, offset, firmwareType)
            return firmware

        try:
            firmware = firmwareClass.fromBinary(binary, None, offset, firmwareType)
            return firmware
        except Exception as ex:
            from UtkBase.biosFile import BiosFile
            if BiosFile.dontHandleExceptions:
                raise ex
            traceback.print_exception(type(ex), ex, ex.__traceback__)

        # Fallback when something went wrong
        # TODO logging that this is a fall-back option. Later i mean
        firmware = FirmwareBlob.fromBinary(binary, None, offset, firmwareType)
        return firmware
