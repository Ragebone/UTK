from UtkAmd.psp.firmware.firmwareInterface import Firmware
from UtkAmd.psp.firmwareTypes import FirmwareType


class FirmwareMap:

    TypeMap: dict[FirmwareType, list[Firmware]] = {}

    @staticmethod
    def addType(type: FirmwareType, firmware: 'Firmware') -> None:
        """


        :return: None
        """

        firmwareList = FirmwareMap.TypeMap.get(type, None)
        if firmwareList is None:
            FirmwareMap.TypeMap[type] = [firmware]
            return

        assert isinstance(firmwareList, list), "Firmware Type Map is not containing a list, how did that happen?"
        firmwareList.append(firmware)


    @staticmethod
    def ownFirmwareMap() -> dict[FirmwareType, list[Firmware]]:
        """

        :return:
        """
        oldMap = FirmwareMap.TypeMap
        FirmwareMap.TypeMap = {}
        return oldMap
