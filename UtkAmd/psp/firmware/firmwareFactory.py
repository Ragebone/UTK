import logging

from UtkAmd.psp.firmware.firmwareHeaders.firmwareHeaderFactory import FirmwareHeaderFactory
from UtkAmd.psp.firmware.firmwareInterface import Firmware
from UtkAmd.psp.firmware.firmwareBlob import FirmwareBlob
from UtkAmd.psp.firmware.signedFirmwareBlob import SignedFirmwareBlob

from UtkAmd.psp.firmwareTypes import FirmwareType


# TODO create a way to "dynamically" add to this
# TODO implement handling of specific firmware like the APOB, APCB and others
FIRMWARE_TYPE_MAPPING = {
}


class FirmwareFactory:
    """
    Factory for AMD PSP specific firmware

    Primary part of all decisions is the firmwareType value in typed-directorEntries.
    """

    @staticmethod
    def fromBinary(firmwareType: FirmwareType, binary: bytes, offset: int) -> Firmware:
        """
        Construct AMD PSP firmware from the given binary

        :param firmwareType: Type value from the TypedDirectoryEntry
        :param binary: Binary to build the firmware from
        :param offset: Offset the firmware is located at in the image
        :return: firmware as an ImageElement
        """
        # TODO this could take a typedDirectoryEntry instead of just the firmwareType

        assert firmwareType is not None, "FirmwareType must not be None"
        assert binary is not None, "Binary must not be None"

        # NOTE: header can be None
        header = FirmwareHeaderFactory.fromBinary(binary)

        firmwareClass: type[Firmware] = FIRMWARE_TYPE_MAPPING.get(firmwareType)

        # Specific firmware handling
        if firmwareClass is not None:
            try:
                firmware = firmwareClass.fromBinary(binary, header, offset, firmwareType)
                return firmware

            except Exception as ex:
                from UtkBase.biosFile import BiosFile
                if BiosFile.dontHandleExceptions:
                    raise ex
                logging.error(ex.__traceback__)
                # traceback.print_exception(type(ex), ex, ex.__traceback__)

        # More generic handling of firmware
        if header is None:
            return FirmwareBlob.fromBinary(binary, header, offset, firmwareType)

        IS_NOT_SIGNED = not header.isFirmwareSigned()
        if IS_NOT_SIGNED:
            return FirmwareBlob.fromBinary(binary, header, offset, firmwareType)

        try:
            signedFirmwareBlob = SignedFirmwareBlob.fromBinary(binary, header, offset, firmwareType)
            return signedFirmwareBlob

        except Exception as ex:
            logging.error(ex.__traceback__)

            from UtkBase.biosFile import BiosFile
            if BiosFile.dontHandleExceptions:
                raise ex

        # Fallback
        # TODO logging that this is a fall-back option.
        logging.info("Fallback for Signed firmware")
        firmware = FirmwareBlob.fromBinary(binary, header, offset, firmwareType)
        return firmware
