import abc
import enum

from UtkAmd.utkAmdInterfaces import UtkAMD
from utkInterfaces import Serializable


class RomId(enum.Enum):
    SpiCs1_L = 0
    SpiCs2_L = 1
    Unknown2 = 2
    Unknown3 = 3


class Writeable(enum.Enum):
    ReadOnly = 0
    Writeable = 1


class DirectoryEntry(Serializable, UtkAMD):
    """
    Common interface for all entries of all Directories including ComboDirectories and SoftFuseChains
    """

    @classmethod
    @abc.abstractmethod
    def fromBinary(cls, binary: bytes) -> 'DirectoryEntry':
        pass

    @abc.abstractmethod
    def getSize(self) -> int:
        pass


class PointDirectoryEntry(DirectoryEntry):
    """
    Common Interface for all directory entries that point or rather, reference something
    """
    @abc.abstractmethod
    def getEntryLocation(self) -> int:
        """Get the offset / point / location / address referenced"""
        pass

    @abc.abstractmethod
    def isPointEntry(self) -> bool:
        """True if the location is outside the Directory"""
        pass


class TypedDirectoryEntry(PointDirectoryEntry):
    """
    Common interface for all directoryEntries that:
    - Reference something
    - Know something's size
    - Know something's type through value in the directoryEntry

    Need the setAsPointEntry method because they can be pointing into our outside a directories content area.
    That can't be known at the time of creation and hence needs to be set later once it is known.
    """
    @abc.abstractmethod
    def getEntryType(self) -> int:
        """Get the Uint8 type value identifying the Type of Entry referenced by the TypedDirectoryEntry"""
        pass

    @abc.abstractmethod
    def getEntrySize(self) -> int:
        """Get the referenced Entries size"""
        pass

    @abc.abstractmethod
    def setAsPointEntry(self, isPointEntry: bool = True) -> None:
        """
        Set the TypedDirectoryEntry as a pointEntry (Bool).
        :param: isPointEntry: optional default True. Set to False for unsetting DirectoryEntry as PointEntry.
        """
        pass
