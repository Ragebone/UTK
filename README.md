# UEFI Tool Kit

An object-oriented package, framework and collection of tools for and around firmware like UEFI images and bios files. 

Heavily influenced by the famous [UEFITool by LongSoft](https://github.com/LongSoft/UEFITool "UEFITool Github repo") and [PSPTool by PSPReverse](https://github.com/PSPReverse/PSPTool "PSPTool Github repo").

## Roadmap

In no particular order

- [x] Initial shallow implementation down to the UEFI volume level 
- [ ] Full implementation down to UEFI files and sections
- [ ] Strings search in framework
- [ ] add JSON serialization via toJson() methods
- [ ] Deterministic export to and import from a directory structure
- [ ] Implement UEFI checksum calculations and verification
- [ ] Crypto system for signature management, verification and signing
- [ ] AMD flavored firmware handling
- [ ] Intel flavored firmware handling
- [ ] HII capability
- [ ] PCD capability
- [ ] NVAR Capability
- [ ] GUID management framework
- [ ] Address and referencing framework
- [ ] Support for emulation and further automation
- [ ] Package release for easy usage

## Architecture



### Factories: 

Figure out, decide what to build specifically and then have it constructed from the given binary.
Decision-making usually happens through checking specific values, offsets or building a Header object.
If possible, the factory is supposed to size-limit the binary given to the object in construction to its actual size.
Sometimes this is not possible, which puts the responsibility of size-limiting on the object.

Important question: 
Does the limited binary still contain the header if it was constructed?
Yes, it has to!

### Specific objects:
- Offer construction from binary and other sources
- Limit themselves to their actual size
- Contain data
- Implement behavior for manipulation
