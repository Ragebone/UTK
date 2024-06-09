import traceback

from UtkBase.images.volumes.files.file import File
from UtkBase.images.volumes.files.fileHeader import FileHeader
from UtkBase.images.volumes.files.sectionedFile import SectionedFile
from UtkBase.images.volumes.files.type import EfiFirmwareFileType
from UtkBase.uefiGuid import UefiGuid
from UtkBase.utility import binaryIsEmpty


SECTIONED_FILE_TYPES = [
    EfiFirmwareFileType.EFI_FV_FILETYPE_SECURITY_CORE,
    EfiFirmwareFileType.EFI_FV_FILETYPE_PEI_CORE,
    EfiFirmwareFileType.EFI_FV_FILETYPE_DXE_CORE,
    EfiFirmwareFileType.EFI_FV_FILETYPE_PEIM,
    EfiFirmwareFileType.EFI_FV_FILETYPE_DRIVER,
    EfiFirmwareFileType.EFI_FV_FILETYPE_COMBINED_PEIM_DRIVER,
    EfiFirmwareFileType.EFI_FV_FILETYPE_APPLICATION,
    EfiFirmwareFileType.EFI_FV_FILETYPE_MM,
    EfiFirmwareFileType.EFI_FV_FILETYPE_FIRMWARE_VOLUME_IMAGE,
    EfiFirmwareFileType.EFI_FV_FILETYPE_COMBINED_MM_DXE,
    EfiFirmwareFileType.EFI_FV_FILETYPE_MM_CORE,
    EfiFirmwareFileType.EFI_FV_FILETYPE_MM_STANDALONE,
    EfiFirmwareFileType.EFI_FV_FILETYPE_MM_CORE_STANDALONE
]


class FileFactory:
    @staticmethod
    def fromBinary(binary: bytes, fileOffset: int = 0) -> File:
        """

        :param binary:
        :return:
        """
        assert binary is not None, "Binary must not be None"

        if len(binary) < FileHeader.size():
            assert binaryIsEmpty(binary), "Volume should be over and filled with FFs, it seems to not be just 0xFFs"
            return None

        try:
            fileHeader = FileHeader.fromBinary(binary)
        except Exception as ex:
            from UtkBase.biosFile import BiosFile
            if BiosFile.dontHandleExceptions:
                raise ex
            traceback.print_exception(type(ex), ex, ex.__traceback__)
            print("Failed parsing FileHeader from binary {}".format(binary))
            return None

        FILE_SIZE = fileHeader.getFileSize()
        FILE_TYPE = fileHeader.getFileType()

        binary = binary[:FILE_SIZE]

        guid: UefiGuid = fileHeader.getGuid()
        if guid.toString() == 'FFFFFFFF-FFFF-FFFF-FFFF-FFFFFFFFFFFF':
            if FILE_SIZE == 0xFFFFFF:
                # Volume content is over and is followed by FFs
                assert binaryIsEmpty(binary), "Volume should be over and filled with FFs, it seems to not be just 0xFFs"
                return None

        if FILE_TYPE in SECTIONED_FILE_TYPES:
            try:
                sectionedFile = SectionedFile.fromBinary(binary, fileHeader, fileOffset)
                return sectionedFile
            except Exception as ex:
                from UtkBase.biosFile import BiosFile
                if BiosFile.dontHandleExceptions:
                    raise ex
                traceback.print_exception(type(ex), ex, ex.__traceback__)
                print("Falling back to generic file that does not parse sections")

        # TODO implement marking files as a Fallback in case there was an issue building SectionedFiles
        file = File.fromBinary(binary, fileHeader, fileOffset)
        return file
