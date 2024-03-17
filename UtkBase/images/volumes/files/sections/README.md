# UEFI Sections

TODO introduction / rambling about sections.


## Architecture 

One software-architectural issue with sections specifically is the amount of shared parsing behavior.
Every Section needs to construct a header for instance.

```python
class Section:
    @classmethod
    def fromBinary(cls, binary: bytes, header: SectionHeader = None) -> 'Section':
        if header is None:
            header = SectionHeaderFactory.fromBinary(binary)

        SECTION_SIZE = header.getSectionSize()
        binary = binary[:SECTION_SIZE]
        BINARY_SIZE = len(binary)
        assert BINARY_SIZE == SECTION_SIZE, "{} has a differing amount of bytes. Expected: {} Got: {}".format(cls.__name__, hex(SECTION_SIZE), hex(BINARY_SIZE))

        # Closed door / open door
        section = cls.process(binary, header)
        return section
```

That has let to the second to last lines implementation detail.

A separate class-method that takes over and continues with the specific sections peculiarities.
Some call this something close to "Closed door, open door".
Something so that an implementation does not need to change anymore.

The only thing left to improve on, is probably the naming!
`process` is not that good a name for it.



