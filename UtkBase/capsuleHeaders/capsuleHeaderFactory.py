from UtkBase.capsuleHeaders.amiAptioCapsuleHeader import AmiAptioCapsuleHeader
from UtkBase.capsuleHeaders.efiCapsuleHeader import EfiCapsuleHeader

EFI_FMP_CAPSULE_GUID = b'\xED\xD5\xCB\x6D\x2D\xE8\x44\x4C\xBD\xA1\x71\x94\x19\x9A\xD9\x2A'                           # Standard FMP capsule GUID
EFI_CAPSULE_GUID = b'\xBD\x86\x66\x3B\x76\x0D\x30\x40\xB7\x0E\xB5\x51\x9E\x2F\xC5\xA0'                               # 6DCBD5ED-E82D-4C44-BDA1-7194199AD92A
INTEL_CAPSULE_GUID = b'\xB9\x82\x91\x53\xB5\xAB\x91\x43\xB6\x9A\xE3\xA9\x43\xF7\x2F\xCC'                             # Standard EFI capsule GUID
LENOVO_CAPSULE_GUID = b'\xD3\xAF\x0B\xE2\x14\x99\x4F\x4F\x95\x37\x31\x29\xE0\x90\xEB\x3C'                            # 3B6686BD-0D76-4030-B70E-B5519E2FC5A0
LENOVO2_CAPSULE_GUID = b'\x76\xFE\xB5\x25\x43\x82\x5C\x4A\xA9\xBD\x7E\xE3\x24\x61\x98\xB5'                           # Intel capsule GUID
TOSHIBA_CAPSULE_GUID = b'\x62\x70\xE0\x3B\x51\x1D\xD2\x45\x83\x2B\xF0\x93\x25\x7E\xD4\x61'                           # 539182B9-ABB5-4391-B69A-E3A943F72FCC
APTIO_SIGNED_CAPSULE_GUID = b'\x8B\xA6\x3C\x4A\x23\x77\xFB\x48\x80\x3D\x57\x8C\xC1\xFE\xC4\x4D'                      # Lenovo capsule GUID
APTIO_UNSIGNED_CAPSULE_GUID = b'\x90\xBB\xEE\x14\x0A\x89\xDB\x43\xAE\xD1\x5D\x3C\x45\x88\xA4\x18'                    # E20BAFD3-9914-4F4F-9537-3129E090EB3C

EFI_FIRMWARE_FILE_SYSTEM_GUID = b'\xD9\x54\x93\x7A\x68\x04\x4A\x44\x81\xCE\x0B\xF6\x17\xD8\x90\xDF'                  # Another Lenovo capsule GUID
EFI_FIRMWARE_FILE_SYSTEM2_GUID = b'\x78\xE5\x8C\x8C\x3D\x8A\x1C\x4F\x99\x35\x89\x61\x85\xC3\x2D\xD3'                 # 25B5FE76-8243-4A5C-A9BD-7EE3246198B5
EFI_FIRMWARE_FILE_SYSTEM3_GUID = b'\x7A\xC0\x73\x54\xCB\x3D\xCA\x4D\xBD\x6F\x1E\x96\x89\xE7\x34\x9A'                 # Toshiba capsule GUID
EFI_APPLE_IMMUTABLE_FV_GUID = b'\xAD\xEE\xAD\x04\xFF\x61\x31\x4D\xB6\xBA\x64\xF8\xBF\x90\x1F\x5A'                    # 3BE07062-1D51-45D2-832B-F093257ED461
EFI_APPLE_AUTHENTICATION_FV_GUID = b'\x8C\x1B\x00\xBD\x71\x6A\x7B\x48\xA1\x4F\x0C\x2A\x2D\xCF\x7A\x5D'               # AMI Aptio signed extended capsule GUID
EFI_APPLE_MICROCODE_VOLUME_GUID = b'\x97\x21\x3D\x15\xBD\x29\xDC\x44\xAC\x59\x88\x7F\x70\xE4\x1A\x6B'                # 4A3CA68B-7723-48FB-803D-578CC1FEC44D
EFI_INTEL_FILE_SYSTEM_GUID = b'\xFF\xFF\x3F\xAD\x8B\xD2\xC4\x44\x9F\x13\x9E\xA9\x8A\x97\xF9\xF0'                     # AMI Aptio unsigned extended capsule GUID
EFI_INTEL_FILE_SYSTEM2_GUID = b'\x70\xCD\xA1\xD6\x33\x4B\x94\x49\xA6\xEA\x37\x5F\x2C\xCC\x54\x37'                    # 14EEBB90-890A-43DB-AED1-5D3C4588A418
EFI_SONY_FILE_SYSTEM_GUID = b'\x56\x41\x49\x4F\xD6\xAE\x64\x4D\xA5\x37\xB8\xA5\x55\x7B\xCE\xEC'                      # Standard file system GUIDs


_NORMAL_EFI_CAPSULE_HEADERS = [
    EFI_CAPSULE_GUID,
    EFI_FMP_CAPSULE_GUID,
    INTEL_CAPSULE_GUID,
    LENOVO_CAPSULE_GUID,
    LENOVO2_CAPSULE_GUID,
]


class CapsuleHeaderFactory:
    """
    Reference https://github.com/LongSoft/UEFITool/blob/b8567d32cc158eb68d900d9a161e92889e643627/common/ffsparser.cpp#L142
    """
    @staticmethod
    def fromBinary(binary: bytes):
        """
        TODO make this not be horrible
        TODO detect and create a CapsuleHeader
        :param binary:
        :return:
        """
        # TODO use UefiGuids for this instead of the raw binary
        capsuleId = binary[0:16]
        if capsuleId in _NORMAL_EFI_CAPSULE_HEADERS:
            return EfiCapsuleHeader.fromBinary(binary)

        if capsuleId == TOSHIBA_CAPSULE_GUID:
            # TODO parse Toshiba specific capsule Header
            return None

        if capsuleId in [APTIO_SIGNED_CAPSULE_GUID, APTIO_UNSIGNED_CAPSULE_GUID]:
            return AmiAptioCapsuleHeader.fromBinary(binary)

        return None


