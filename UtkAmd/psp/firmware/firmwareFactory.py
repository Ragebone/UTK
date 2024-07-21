import traceback

from UtkAmd.psp.firmware.firmwareHeaders.firmwareHeaderFactory import FirmwareHeaderFactory
from UtkAmd.psp.firmware.firmwareInterface import Firmware
from UtkAmd.psp.firmware.firmwareHeaders.pspFirmwareHeader import PspFirmwareHeader
from UtkAmd.psp.firmware.publicKeys.publicKey import PublicKey
from UtkAmd.psp.firmware.firmwareBlob import FirmwareBlob
from UtkAmd.psp.firmware.signatures.signature import Signature
from UtkAmd.psp.firmwareTypes import FirmwareType


# TODO create a way to "dynamically" add to this
FIRMWARE_TYPE_MAPPING = {
    FirmwareType.AMD_PUBLIC_KEY: PublicKey,
    FirmwareType.AMD_SEC_DBG_PUBLIC_KEY: PublicKey,
    FirmwareType.OEM_PSP_FW_PUBLIC_KEY: PublicKey,
    FirmwareType.BIOS_RTM_SIGNATURE: Signature,
}


class FirmwareFactory:
    """
    Factory for AMD PSP specific firmware

    Primary part of all decisions is the firmwareType vale in typed-directorEntries.
    TODO implement handling of specific firmware like the APOB, APCB and others
    """

    @staticmethod
    def fromBinary(firmwareType: FirmwareType, binary: bytes, offset: int) -> Firmware:
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

        firmwareClass: type[Firmware] = FIRMWARE_TYPE_MAPPING.get(firmwareType)

        # NOTE: header can be None
        header = FirmwareHeaderFactory.fromBinary(binary)

        # TODO once it is an error to handle things just as a firmwareBlob,  remove this.
        if firmwareClass is None:
            firmware = FirmwareBlob.fromBinary(binary, header, offset, firmwareType)
            return firmware

        try:
            firmware = firmwareClass.fromBinary(binary, header, offset, firmwareType)
            return firmware
        except Exception as ex:
            from UtkBase.biosFile import BiosFile
            if BiosFile.dontHandleExceptions:
                raise ex
            traceback.print_exception(type(ex), ex, ex.__traceback__)

        # Fallback when something went wrong
        # TODO logging that this is a fall-back option. Later i mean
        firmware = FirmwareBlob.fromBinary(binary, header, offset, firmwareType)
        return firmware
