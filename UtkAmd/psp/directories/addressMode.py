import enum


class AddressMode(enum.Enum):
    """

    """

    PhysicalX86 = 0             # X86 Physical address
    FlashOffset = 1             # offset from start of BIOS (flash offset)
    DirectoryOffset = 2         # offset from start of directory header
    PartitionOffset = 3         # offset from start of partition

