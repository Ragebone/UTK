from UtkAmd.psp.firmware.firmwareBlob import FirmwareBlob
from UtkAmd.psp.firmwareTypes import FirmwareType
from UtkCommon.interfaces.header import Header


class KeyStore(FirmwareBlob):
    def __init__(self, offset: int, binary: bytes, firmwareType: FirmwareType, header: Header = None):
        super().__init__(offset, binary, firmwareType, header)
