import enum


class FirmwareType(enum.Enum):
    """
    Type value enum for PSP and BIOS directory entries
    """

    #
    #
    # ---- Bios Directory Type values ----
    #
    #
    BIOS_PUBLIC_KEY = 0x05
    """
    Entry points to BIOS public key stored in SPI space.
    Aliased by BIOS_PUBLIC_KEY_V1
    Difference being the location, this type is used in BiosDirectory Entries
    where as V1 is being used in PspDirectoryEntries of older ZEN CPUs. 
    """

    BIOS_RTM_SIGNATURE = 0x07
    """
    Entry points to signed BIOS RTM hash stored  in SPI space
    Aliased by BIOS_RTM_SIGNATURE_V1
    Difference being the location, this type is used in BiosDirectory Entries
    where as V1 is being used in PspDirectoryEntries of older ZEN CPUs. 
    """
    
    MAN_OS = 0x5C
    """
    PSP entry points to manageability OS binary
    """

    MAN_IP_LIB = 0x5D
    """
    PSP entry points to manageability proprietary IP library
    """

    MAN_CONFIG = 0x5E
    """
    PSP entry points to manageability configuration inforamtion
    """

    BIOS_APCB_INFO = 0x60
    """
    Agesa PSP Customization Block (APCB)
    """

    BIOS_APOB_INFO = 0x61
    """
    Agesa PSP Output Block (APOB) target location
    """

    BIOS_FIRMWARE = 0x62
    """
    BIOS Firmware volumes
    """

    APOB_NV_COPY = 0x63
    """
    APOB data copy on non-volatile storage which will used by ABL during S3 resume
    """

    PMU_INSTRUCTION = 0x64
    """
    Location field pointing to the instruction portion of PMU firmware
    """

    PMU_DATA = 0x65
    """
    Location field pointing to the data portion of PMU firmware
    """

    UCODE_PATCH = 0x66
    """
    Microcode patch
    """

    CORE_MCEDATA = 0x67
    """
    Core MCE data
    """

    BIOS_APCB_INFO_BACKUP = 0x68           
    """
    Backup Agesa PSP Customization Block (APCB)
    """

    BIOS_DIR_LV2 = 0x70
    """
    BIOS entry points to Level 2 BIOS DIR
    """

    DISCRETE_USB4_FIRMWARE = 0x71
    """
    Discrete USB4 Firmware volumes
    """

    PSP_RIB = 0x76
    """
    ID: 0x76, PSP entry points to RIB FW
    """
    
    PSP_BOOT_OEM_TRUSTLET = 0x80
    """
    ID: 0x80, PSP entry points to boot-loaded OEM trustlet binary
    """
    
    PSP_BOOT_OEM_TRUSTLET_KEY = 0x81
    """
    ID: 0x81, PSP entry points to key of the boot-loaded OEM trustlet binary
    """
    
    MPM_FW_1 = 0x85
    """
    ID: 0x85, AMF Firmware part 1: Lx core can start execution only from SRAM
    also part 1 FW will be used to initialize MPM TLB's so that DRAM can be mapped to Lx
    """
    
    MPM_FW_2 = 0x86
    """
    ID: 0x86, AMF Firmware part 2: Bulk of MPM functionality will be implemented in this part
    """
    
    MPM_PERSISTENT_STORAGE = 0x87
    """
    ID: 0x87, Persistent storage exclusively for AIM-T needs
    """
    
    MPM_WLAN_FW = 0x88
    """
    ID: 0x88, WLAN firmware copied to MPM memory by MFD and then MPM will send this to WLAN
    """
    
    PSP_MMPDMA = 0x8C
    """
    ID: 0x8C, PSP entry points to TigerFish MMPDMA FW.
    """
    
    PSP_GMI = 0x91
    """
    ID: 0x91, PSP entry points to MPDMA Page Migration FW
    """
    
    PSP_PM = 0x92
    """
    ID: 0x92, PSP entry points to GMI FW
    """
    
    PMF_BINARY = 0x99
    """
    ID: 0x99, Binary that contains PMF policy
    """

    #
    #
    # ---- PSP Directory Type values ----
    #
    #
    AMD_PUBLIC_KEY = 0x00
    """
    ID: 0x00, PSP entry pointer to AMD public key
    """
    
    PSP_FW_BOOT_LOADER = 0x01
    """
    ID: 0x01, PSP entry points to PSP boot loader in SPI space
    """
    
    PSP_FW_TRUSTED_OS = 0x02
    """
    ID: 0x02, PSP entry points to PSP Firmware region in SPI space
    """
    
    PSP_FW_RECOVERY_BOOT_LOADER = 0x03
    """
    ID: 0x03, PSP entry point to PSP recovery region.
    """
    
    PSP_NV_DATA = 0x04
    """
    ID: 0x04, PSP entry points to fTPM data region in SPI space
    """

    # V1 Type values
    BIOS_PUBLIC_KEY_V1 = 0x05
    """
    ID: 0x05, Entry points to BIOS public key stored in SPI space.
    
    Aliases BIOS_PUBLIC_KEY type value.
    Difference being the location, this type is used in PspDirectoryEntries Entries with early ZEN CPUs.
    """
    
    BIOS_RTM_FIRMWARE_V1 = 0x06
    """
    ID: 0x06, PSP entry points to BIOS RTM code (PEI volume) in SPI space
    Does not seem to have a modern BiosDirectoryEntry replacement
    """
    
    BIOS_RTM_SIGNATURE_V1 = 0x07
    """
    ID: 0x07, PSP entry points to signed BIOS RTM hash stored  in SPI space
    
    Aliases BIOS_RTM_SIGNATURE type value.
    Difference being the location, this type is used in PspDirectoryEntries Entries with early ZEN CPUs.
    """
    
    SMU_OFFCHIP_FW = 0x08
    """
    ID: 0x08, PSP entry points to SMU image
    """
    
    AMD_SEC_DBG_PUBLIC_KEY = 0x09
    """
    ID: 0x09, PSP entry pointer to Secure Unlock Public key
    """
    
    OEM_PSP_FW_PUBLIC_KEY = 0x0A
    """
    ID: 0x0A, PSP entry pointer to an optional public part of the OEM PSP Firmware Signing Key Token
    """
    
    AMD_SOFT_FUSE_CHAIN_01 = 0x0B
    """
    ID: 0x0B, PSP entry pointer to 64bit PSP Soft Fuse Chain
    """
    
    PSP_BOOT_TIME_TRUSTLETS = 0x0C
    """
    ID: 0x0C, PSP entry points to boot-loaded trustlet binaries
    """
    
    PSP_BOOT_TIME_TRUSTLETS_KEY = 0x0D
    """
    ID: 0x0D, PSP entry points to key of the boot-loaded trustlet binaries
    """
    
    PSP_AGESA_RESUME_FW = 0x10
    """
    ID: 0x10, PSP Entry points to PSP Agesa-Resume-Firmware
    """
    
    SMU_OFF_CHIP_FW_2 = 0x12
    """
    ID: 0x12, PSP entry points to secondary SMU image
    """
    
    PSP_EARLY_UNLOCK_DEBUG_IMAGE = 0x13
    """
    ID: 0x13, PSP entry points to PSP early secure unlock debug image
    """
    
    PSP_S3_NV_DATA = 0x1A
    """
    ID: 0x1A, PSP entry pointer to S3 Data Blob
    """
    
    HW_IP_CONFIG_FILE = 0x20
    """
    ID: 0x20, PSP entry points to HW IP configuration file
    """
    
    WRAPPED_IKEK = 0x21
    """
    ID: 0x21, PSP entry points to Wrapped iKEK
    """
    
    PSP_TOKEN_UNLOCK_DATA = 0x22
    """
    ID: 0x22, PSP entry points to PSP token unlock data
    """
    
    PSP_DIAG_BOOT_LOADER = 0x23
    """
    ID: 0x23, PSP entry points to PSP Diag BL on non-secure part via fuse
    """
    
    SECURE_GASKET_BINARY = 0x24
    """
    ID: 0x24, PSP entry points to security gasket binary
    """

    UNKNOWN_25 = 0x25
    """
    Yet unknown
    """

    UNKNOWN_28 = 0x28
    """
    Yet unknown
    """

    KVM_ENGINE_BINARY = 0x29
    """
    ID: 0x29, PSP entry points to PSP KVM Engine binary
    """

    MP5_FW = 0x2A
    """
    MP5 FW According to the PSPTool
    """

    TEE_WONE_NVRAM = 0x2C
    """
    ID: 0x2C, PSP entry points to TEE_WONE_NVRAM binary
    """

    UNKNOWN_2 = 0x2E
    """
    Yet unknown
    """

    EXTERNAL_PREMIUM_CHIPSET_MP1_FW = 0x2F
    """
    ID: 0x2F, PSP entry points to External Premium Chipset MP0 FW image
    """
    
    AGESA_BOOT_LOADER_0 = 0x30
    """
    ID: 0x30, PSP entry points to PSP AGESA Binary 0
    """
    
    AGESA_BOOT_LOADER_1 = 0x31
    """
    ID: 0x31, PSP entry points to PSP AGESA Binary 1
    """
    
    AGESA_BOOT_LOADER_2 = 0x32
    """
    ID: 0x32, PSP entry points to PSP AGESA Binary 2
    """
    
    AGESA_BOOT_LOADER_3 = 0x33
    """
    ID: 0x33, PSP entry points to PSP AGESA Binary 3
    """
    
    AGESA_BOOT_LOADER_4 = 0x34
    """
    ID: 0x34, PSP entry points to PSP AGESA Binary 4
    """
    
    AGESA_BOOT_LOADER_5 = 0x35
    """
    ID: 0x35, PSP entry points to PSP AGESA Binary 5
    """
    
    AGESA_BOOT_LOADER_6 = 0x36
    """
    ID: 0x36, PSP entry points to PSP AGESA Binary 6
    """
    
    AGESA_BOOT_LOADER_7 = 0x37
    """
    ID: 0x37, PSP entry points to PSP AGESA Binary 7
    """
    
    PSP_VM_GUARD_DATA = 0x38
    """
    ID: 0x38, PSP entry points to VM Guard data
    """
    
    PSP_SEV = 0x39
    """
    ID: 0x39, PSP entry points to SEV binary
    """
    
    PSP_DIR_LV2 = 0x40
    """
    ID: 0x40, PSP entry points to Level 2 PSP DIR
    """
    
    PSP_PHY = 0x42
    """
    ID: 0x42, PSP entry points to PHY binary
    """

    UNKNOWN_0 = 0x43
    """
    Yet unknown
    """

    UNKNOWN_44 = 0x44
    """
    Yet unknown
    """

    UNKNOWN_45 = 0x45
    """
    Yet unknown
    """

    EXTERNAL_PREMIUM_CHIPSET_PSP_BL = 0x46
    """
    ID: 0x46, PSP entry points to External Premium Chipset PSP Boot Loader
    """

    DRTM_TA = 0x47
    """
    DRTM_TA  ?   PSPTOOL sais so
    """
    
    PSP_REGION_A_DIR = 0x48
    """
    ID: 0x48, PSP entry points to PSP DIR in Region A
    """
    
    BIOS_REGION_DIR = 0x49
    """
    ID: 0x49, PSP entry points to BIOS DIR in Region A or B
    """
    
    PSP_REGION_B_DIR = 0x4A
    """
    ID: 0x4A, PSP entry points to PSP DIR in Region B
    """

    UNKNOWN_4C = 0x4C
    """
    Yet unknown
    """

    UNKNOWN_4D = 0x4D
    """
    Yet unknown
    """

    UNKNOWN_4E = 0x4E
    """
    Yet unknown
    """

    UNKNOWN_50 = 0x50
    """
    Yet unknown
    """

    TOS_PUBLIC_KEY = 0x51
    """
    PSPTOOL: TOS_PUBLIC_KEY
    """

    PSP_NVRAM = 0x54
    """
    ID: 0x54, PSP entry points to PSP NVRAM for RPMC
    """

    BL_ROLLBACK_SPL = 0x55
    """
    PSPTOOL sais BL_ROLLBACK_SPL
    """

    MSMU_BINARY_0 = 0x5A
    """
    ID: 0x5A, PSP entry points to MSMU
    """
    
    PSP_MPIO = 0x5D
    """
    ID: 0x5D, PSP entry points to MPIO Offchip Firmware
    """
    
    AMD_SCS_BINARY = 0x5F
    """
    ID: 0x5F, Software Configuration Settings Data Block
    """
    
    AMD_SFFS_BINARY = 0x63
    """
    ID: 0x63, Secure Coprocessor Enforced System Firmware
    Provides an authenticated mechanism to enable and customize system level firmware/software features.
    """

    UNKNOWN_6A = 0x6A
    """
    Yet unknown
    """
