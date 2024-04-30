from UtkAmd.psp.directories.biosDirectory import BiosDirectory
from UtkAmd.psp.directories.comboDirectory import ComboDirectory
from UtkAmd.psp.directories.directoryHeaders.comboDirectoryHeader import ComboDirectoryHeader
from UtkAmd.psp.directories.directoryHeaders.pspDirectoryHeader import PspDirectoryHeader
from UtkAmd.psp.directories.directory import Directory
from UtkAmd.psp.directories.pspDirectory import PspDirectory

DIRECTORY_CLASS_MAPPING = {
    # psp
    b'2PSP': ComboDirectory,
    b'$PSP': PspDirectory,                  # level 1
    b'$PL2': PspDirectory,                  # level 2

    # Bios
    b'2BHD': ComboDirectory,
    b'$BHD': BiosDirectory,                 # level 1
    b'$BL2': BiosDirectory                  # level 2
}


class DirectoryFactory:
    """
    Factory for building Zen PSP Directory-objects
    """

    @staticmethod
    def isDirectory(binary: bytes) -> tuple[bool, bytes]:
        """
        Determines if the given binary starts with a Directory structure

        :param binary: Binary to be checked
        :return: A tuple of: Bool (True if it is a directory), the found directory Signature.
        """
        assert binary is not None, "Received None as binary"
        signature = binary[:4]
        return signature in DIRECTORY_CLASS_MAPPING, signature

    @staticmethod
    def fromBinary(binary: bytes, offset: int) -> Directory:
        assert binary is not None, "None as binary"

        isDirectory, signature = DirectoryFactory.isDirectory(binary)
        if not isDirectory:
            # TODO  is returning None better then asserting?
            return None

        if signature in [b'2PSP', b'2BHD']:
            comboDirectoryHeader = ComboDirectoryHeader.fromBinary(binary)
            comboDir = ComboDirectory.fromBinary(binary, comboDirectoryHeader, offset)
            return comboDir

        directoryHeader = PspDirectoryHeader.fromBinary(binary)
        dirClass = DIRECTORY_CLASS_MAPPING.get(signature)
        directory = dirClass.fromBinary(binary, directoryHeader, offset)
        return directory
