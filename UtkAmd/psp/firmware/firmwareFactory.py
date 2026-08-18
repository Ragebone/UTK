import logging

from UtkAmd.psp.firmware.firmwareHeaders.firmwareHeaderFactory import FirmwareHeaderFactory
from UtkAmd.psp.firmware.firmwareInterface import Firmware
from UtkAmd.psp.firmware.firmwareBlob import FirmwareBlob
from UtkAmd.psp.firmware.keyStore.keyStoreFile import KeyStoreFile
from UtkAmd.psp.firmware.publicKeys.amdPublicKey import AmdPublicKey
from UtkAmd.psp.firmware.signedFirmwareBlob import SignedFirmwareBlob

from UtkAmd.psp.firmwareTypes import FirmwareType

# TODO very useful for types: https://github.com/Mimoja/PSP-Entry-Types/blob/master/types.csv

# TODO create a way to "dynamically" add to this
# TODO implement handling of specific firmware like the APOB, APCB and others
FIRMWARE_TYPE_MAPPING = {
    FirmwareType.AMD_PUBLIC_KEY: AmdPublicKey,
    FirmwareType.UNKNOWN_50: KeyStoreFile,
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
        from UtkAmd.psp.firmwareMap import FirmwareMap
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

                FirmwareMap.addType(firmwareType, firmware)
                return firmware

            except Exception as ex:
                from UtkBase.biosFile import BiosFile
                if BiosFile.dontHandleExceptions:
                    raise ex
                logging.error(ex.__traceback__)
                # traceback.print_exception(type(ex), ex, ex.__traceback__)

        # More generic handling of firmware
        if header is None:
            firmware = FirmwareBlob.fromBinary(binary, header, offset, firmwareType)
            FirmwareMap.addType(firmwareType, firmware)
            return firmware

        IS_NOT_SIGNED = not header.isFirmwareSigned()
        if IS_NOT_SIGNED:
            firmware = FirmwareBlob.fromBinary(binary, header, offset, firmwareType)
            FirmwareMap.addType(firmwareType, firmware)
            return firmware

        try:
            signedFirmwareBlob = SignedFirmwareBlob.fromBinary(binary, header, offset, firmwareType)
            FirmwareMap.addType(firmwareType, signedFirmwareBlob)
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
        FirmwareMap.addType(firmwareType, firmware)
        return firmware
