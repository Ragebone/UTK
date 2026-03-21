import ctypes
from ctypes import LittleEndianStructure

from cryptography.utils import Enum


class leStructure(LittleEndianStructure):
    @classmethod
    def _fieldToDict(cls, name: str, value: any) -> any:
        """Convert a single field value to JSON-serializable format."""
        if isinstance(value, bytes):
            return value.hex().upper()
        if isinstance(value, (ctypes.Array,)):
            return bytes(value).hex().upper()
        if isinstance(value, int):
            return hex(value)
        if isinstance(value, Enum):
            return {"name": value.name, "value": value.value}
        return value

    @classmethod
    def _fieldFromDict(cls, field_type: type, value: any) -> any:
        """Convert a dictionary value back to the correct field type."""
        # Handle hex strings
        if isinstance(value, str) and value.startswith('0x'):
            if isinstance(field_type, type) and issubclass(field_type, ctypes._SimpleCData):
                return field_type(int(value, 16))
            return int(value, 16)

        # Handle byte arrays (ctypes.Array)
        if isinstance(value, str) and not value.startswith('0x'):
            # Assume it's a hex string for byte arrays
            byte_data = bytes.fromhex(value)
            if hasattr(field_type, '_length_'):
                return field_type.from_buffer_copy(byte_data)
            return byte_data

        return value

    def toDict(self) -> dict[str, any]:
        """
        Convert ctypes structure to dictionary with hex-encoded binary values.
        """
        result = {}
        for field_name, field_type in self._fields_:
            value = getattr(self, field_name)
            result[field_name] = self._fieldToDict(field_name, value)
        return result

    @classmethod
    def fromDict(cls, data: dict[str, any]) -> 'CtypesStructureHelper':
        """
        Reconstruct ctypes structure from dictionary.
        """
        instance = cls()
        for field_name, field_type in cls._fields_:
            if field_name not in data:
                continue

            value = data[field_name]
            converted_value = cls._fieldFromDict(field_type, value)
            setattr(instance, field_name, converted_value)

        return instance