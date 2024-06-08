import abc

from UtkAmd.psp.addressMode import AddressMode
from UtkAmd.utkAmdInterfaces import UtkAMD
from utkInterfaces import Header


class DirectoryHeader(Header, UtkAMD):
    """
    Interface for Directory Headers
    Specific implementations in:
    - ComboDirectoryHeader  for Combo directories
    - PspDirectoryHeader    for Psp and Bios directories
    """

    @classmethod
    @abc.abstractmethod
    def fromBinary(cls, binary: bytes) -> 'DirectoryHeader':
        pass

    @abc.abstractmethod
    def getEntryCount(self) -> int:
        """Get the number of DirectoryEntries of the Directory"""
        pass

    @abc.abstractmethod
    def getSize(self):
        """Get the Size of the Header"""
        pass

    @abc.abstractmethod
    def getAddressMode(self) -> AddressMode:
        """Can to be None. Get the AddressMode of the Header which should be relevant for the hole directory"""
        pass

    @abc.abstractmethod
    def getSignature(self) -> bytes:
        """
        Retrieve the Headers Signature as bytes.
        Useful for validating the directory and header fit together
        """
        pass
