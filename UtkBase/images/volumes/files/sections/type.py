import enum


class SectionType(enum.Enum):
    """
    Enum for Section-Types
    """
    ALL = 0x00
    Compressed = 0x01
    GuidDefined = 0x02
    Disposable = 0x03

    PE32 = 0x10
    PIC = 0x11
    TE = 0x12
    DxeDepex = 0x13
    Version = 0x14
    UserInterface = 0x15
    Compatibility16 = 0x16
    FirmwareVolumeImage = 0x17
    FreeformSubtypeGuid = 0x18
    Raw = 0x19

    PeiDepex = 0x1B
    MmDepex = 0x1C
