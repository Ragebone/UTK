from ctypes import LittleEndianStructure, c_uint32, c_byte, c_char

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey

from UtkAmd.psp.keyMap import KeyMap
from UtkAmd.utkAmdInterfaces import UtkAMD
from UtkCommon.interfaces.header import Header

HEADER_SIZE = 0x50

class KeyStoreHeader(LittleEndianStructure, Header, UtkAMD):
    _fields_ = [
        ("_size", c_uint32),                         # 0 - 3
        ("_unknown_flag", c_uint32),                 # 4 - 7
        ("_magic", c_char * 4),                      # 8 - 11
        ("_reserved", c_byte * 0x44),                # 12 -
    ]

    @classmethod
    def fromBinary(cls, binary: bytes) -> 'KeyStoreHeader':
        headerBinary = binary[:HEADER_SIZE]
        assert len(headerBinary) == HEADER_SIZE, "To few bytes for KeyStoreHeader, got: {}".format(binary)

        header = cls.from_buffer_copy(headerBinary)
        assert bytes(header._magic) == b'$KDB', f"KeyStoreHeader MAGIC missmatch; {header._magic} should be $KDB"
        assert bytes(header._reserved) == b'\0' * 0x44, "KeyStoreHeader reserved bytes aren't all 0"

        return header

class KeyStore:
    """
    Body of the KeyStoreFile - usually signed in the keyStoreFile
    """
    @classmethod
    def fromBinary(cls, binary: bytes, header: KeyStoreHeader = None):
        if header is None:
            header = KeyStoreHeader.fromBinary(binary[:HEADER_SIZE])
        body = binary[HEADER_SIZE:]

        entries = []
        workBin = body
        # TODO parse header first, check validity, then hand the limited binary to the entry
        while True:
            if len(workBin) < ENTRY_HEADER_SIZE:
                break

            keyHeader = EntryHeader.fromBinary(workBin)
            keySize = keyHeader.getEntrySize()
            entry_bin = workBin[:keySize]
            if len(entry_bin) != keySize:
                break

            key = Entry.fromBinary(entry_bin, keyHeader)
            entries.append(key)
            workBin = workBin[keySize:]

        return cls(binary, header, entries)

    def __init__(self, binary, header: KeyStoreHeader, entries):
        self._binary = binary
        self._header = header
        self._entries = entries



ENTRY_HEADER_SIZE = 0x50


class EntryHeader(LittleEndianStructure, Header, UtkAMD):
    _fields_ = [
        ("_size", c_uint32),                         # 0 - 3
        ("_unknown_flag", c_uint32),                 # 4 - 7
        ("_unknown_id", c_uint32),                   # 8 - 11
        ("_rsa_exponent", c_uint32),                 # 12 - 15
        ("_key_id", c_char * 0x10),                  # 16 - 0x1F
        ("_key_size", c_uint32),                     # 0x20 - 0x23
        ("_reserved",  c_byte * 0x24),               # 0x24 - 0x38
        ("_possible_version", c_uint32),             # 0x  TODO fix those numbers here.
        # b'\0' * 0x2b  + b'\0', seems to be how many 0es and then a version number
    ]

    @classmethod
    def fromBinary(cls, binary: bytes) -> 'EntryHeader':
        headerBinary = binary[:ENTRY_HEADER_SIZE]
        assert len(headerBinary) == ENTRY_HEADER_SIZE, f"To few bytes for {cls}, got: {binary}"

        header = cls.from_buffer_copy(headerBinary)
        # assert header._unknown_id < 0x100, f"Unknown ID too large, got: {header._unknown_id}"
        # assert header._rsa_exponent == 0x10001, f"RSA exponent is {header._rsa_exponent} instead of 0x10001"
        return header

    def getEntrySize(self) -> int:
        return self._size

    def getExponent(self):
        return self._rsa_exponent

    def getKeyId(self) -> bytes:
        return bytes(self._key_id)

    def getKeyIdString(self) -> str:
        return self.getKeyId().hex().upper()


class Entry:
    @classmethod
    def fromBinary(cls, binary: bytes, header: EntryHeader = None) -> 'Entry':
        if header is None:
            header = EntryHeader.fromBinary(binary)

        size = header.getEntrySize()
        binary = binary[:size]
        assert len(binary) == size , "Fewer bytes then EntryHeader specifies"

        body = binary[ENTRY_HEADER_SIZE:]
        assert len(body) > 0, "Body too short for Keys"

        publicKeyExponent = header.getExponent()
        publicKeyModulus = int.from_bytes(body, "little")
        rsaPublicKey: RSAPublicKey = rsa.RSAPublicNumbers(publicKeyExponent, publicKeyModulus).public_key()

        entry = cls(header, rsaPublicKey)
        KeyMap.addKey(header.getKeyIdString(), entry)
        return entry

    def __init__(self, header: EntryHeader, rsaPublicKey: RSAPublicKey):
        self._header = header
        self._rsaPublicKey = rsaPublicKey

    def getSize(self):
        return self._header.getEntrySize()
