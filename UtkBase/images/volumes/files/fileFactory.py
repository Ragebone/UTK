from UtkBase.images.volumes.files.file import File
from UtkBase.images.volumes.files.fileHeader import FileHeader
from UtkBase.uefiGuid import UefiGuid
from UtkBase.utility import binaryIsEmpty


class FileFactory:
    @staticmethod
    def fromBinary(binary: bytes):
        """

        :param binary:
        :return:
        """
        assert binary is not None, "Binary must not be None"
        fileHeader = FileHeader.fromBinary(binary)

        FILE_SIZE = fileHeader.getFileSize()
        binary = binary[:FILE_SIZE]

        guid: UefiGuid = fileHeader.getGuid()
        if guid.toString() == 'FFFFFFFF-FFFF-FFFF-FFFF-FFFFFFFFFFFF':
            if FILE_SIZE == 0xFFFFFF:
                # Volume content is over and is followed by FFs
                assert binaryIsEmpty(binary), "Volume should be over and filled with FFs, it seems to not be just 0xFFs"
                return None

        file = File.fromBinary(binary, fileHeader)
        return file
