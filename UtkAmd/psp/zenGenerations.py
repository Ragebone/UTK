import enum


class ZenGeneration(enum.Enum):
    """
      ZEN_GENERATION_IDS = {'Zen 1'  : [b'\x00\x09\xBC', b'\x00\x0A\xBC'],
                          'Zen 2'  : [b'\x05\x0B\xBC', b'\x01\x0A\xBC'],
                          'Zen 3'  : [b'\x01\x0C\xBC', b'\x00\x0C\xBC'],
                          'Zen 4'  : [b'\x04\x0D\xBC', b'\x0B\x0D\xBC'],
                          'Zen 4/5': [b'\x03\x0D\xBC']
                         }
    """
    ZEN1_0 = b'\x00\x09\xBC'
    ZEN1_1 = b'\x00\x0A\xBC'

    ZEN2_0 = b'\x05\x0B\xBC'
    ZEN2_1 = b'\x01\x0A\xBC'

    ZEN3_0 = b'\x01\x0C\xBC'
    ZEN3_1 = b'\x00\x0C\xBC'

    ZEN4_0 = b'\x04\x0D\xBC'
    ZEN4_1 = b'\x0B\x0D\xBC'

    ZEN4or5 = b'\x03\x0D\xBC'

    STRIX_HALO = b'\t\x0e\xbc'




