# UEFI Tool Kit

An object-oriented package, framework and collection of tools for and around firmware like UEFI images and bios files. 

Heavily influenced by the famous [UEFITool by LongSoft](https://github.com/LongSoft/UEFITool "UEFITool Github repo") and [PSPTool by PSPReverse](https://github.com/PSPReverse/PSPTool "PSPTool Github repo").

## Roadmap

In no particular order

- [x] Initial shallow implementation down to the UEFI volume level 
- [ ] add JSON serialization via toJson() methods
- [ ] Full implementation down to UEFI files and sections
- [ ] Deterministic export to and import from a directory structure
- [ ] Implement UEFI checksum calculations and verification
- [ ] Crypto system for signature management, verification and signing
- [ ] AMD flavored firmware handling
- [ ] Intel flavored firmware handling
- [ ] HII capability
- [ ] PCD capability
- [ ] NVAR Capability
- [ ] Strings search in framework
- [ ] GUID management framework
- [ ] Address and referencing framework
- [ ] Support for emulation and further automation
- [ ] Package release for easy usage