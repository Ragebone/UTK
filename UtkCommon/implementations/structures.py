import ctypes
from ctypes import LittleEndianStructure
from difflib import get_close_matches


class CaseInsensitiveDict(dict):
    """Dictionary with case-insensitive key access and typo suggestions."""

    def __getitem__(self, key):
        if isinstance(key, str):
            # Try exact match first
            for k in self.keys():
                if isinstance(k, str) and k.lower() == key.lower():
                    return super().__getitem__(k)
        return super().__getitem__(key)

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def __contains__(self, key):
        if isinstance(key, str):
            return any(isinstance(k, str) and k.lower() == key.lower() for k in self.keys())
        return super().__contains__(key)

    def _suggest_key(self, missing_key: str) -> str:
        """Find and return a similar key if it exists."""
        matches = get_close_matches(missing_key, self.keys(), n=1, cutoff=0.6)
        if matches:
            return matches[0]
        return None


class leStructure(LittleEndianStructure):
    """
    Base class for ctypes LittleEndianStructure with dict conversion helpers.
    Subclasses should implement toDict() with custom field mapping.
    fromDict() provides case-insensitive loading with typo suggestions.
    """

    @staticmethod
    def _fieldToValue(value: any) -> any:
        """Convert a field value to JSON-serializable format."""
        if isinstance(value, bytes):
            return value.hex().upper()

        if isinstance(value, ctypes.Array):
            return bytes(value).hex().upper()

        if isinstance(value, int):
            return hex(value)

        return value

    @staticmethod
    def _fieldFromValue(field_type: type, value: any) -> any:
        """Convert a dictionary value to the correct field type."""
        if value is None:
            return None

        if isinstance(value, str):
            if value.startswith('0x'):
                try:
                    return int(value, 16)
                except (ValueError, TypeError):
                    return value
            else:
                # Try hex decode for byte arrays
                try:
                    byte_data = bytes.fromhex(value)
                    if hasattr(field_type, '_length_'):
                        return field_type.from_buffer_copy(byte_data)
                    return byte_data
                except (ValueError, TypeError):
                    return value

        return value

    @classmethod
    def fromDict(cls, data: dict[str, any]) -> 'leStructure':
        """
        Reconstruct structure from dictionary with case-insensitive keys.
        Suggests corrections for typos in missing keys.
        """
        data_ci = CaseInsensitiveDict(data)
        instance = cls()

        for field_name, field_type in cls._fields_:
            if field_name not in data_ci:
                suggested = data_ci._suggest_key(field_name)
                if suggested:
                    raise KeyError(
                        f"Field '{field_name}' not found in data. "
                        f"Did you mean '{suggested}'?"
                    )
                continue

            value = data_ci[field_name]
            converted = cls._fieldFromValue(field_type, value)
            setattr(instance, field_name, converted)

        return instance