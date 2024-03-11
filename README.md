# UEFI Tool Kit

An object-oriented package, framework and collection of tools for and around firmware like UEFI images and bios files. 

Heavily influenced by the famous [UEFITool by LongSoft](https://github.com/LongSoft/UEFITool "UEFITool Github repo") and [PSPTool by PSPReverse](https://github.com/PSPReverse/PSPTool "PSPTool Github repo").
Noteworthy as well: [uefi-firmware-parser](https://github.com/theopolis/uefi-firmware-parser "Github repo")

## Roadmap

In no particular order

- [x] Initial shallow implementation down to the UEFI volume level 
- [x] Rough implementation down to UEFI files and sections, even compressed ones
- [x] Basic-ish documentation in README.md files
- [x] UEFI GUID database and name support
- [ ] GUID management framework
- [ ] Full implementation down to UEFI files and sections
- [ ] Full implementation down to decompression and compression 
- [ ] Strings search in framework
- [ ] JSON serialization via toJson() methods
- [ ] Deterministic export to and import from a directory structure
- [ ] Implement UEFI checksum calculations and verification
- [ ] Crypto system for signature management, verification and signing
- [ ] AMD flavored firmware handling
- [ ] Intel flavored firmware handling
- [ ] HII capability
- [ ] PCD capability
- [ ] NVAR Capability
- [ ] Address and referencing framework
- [ ] Support for emulation and further automation
- [ ] Package release for easy usage
- [ ] Actual tools and use-cases

## Architecture

Each folder attempts to contain only what the respective UEFI thing is made up from.

What ever the UEFI thing contains, is then supposed to be in a subdirectory hopefully aptly named.

README.md documents in each directory are supposed to contain further information. 

The current directory structure:

```
UTK
├── images/
├── tests/
├── tools/
├── UtkBase/
├── .gitignore
└── README.md
```

- `images/` is ignored by git.
   Place any cap, bios or uefi image files here to be used in your local testing.


- `tests/` for python unit-tests.
   Currently only contains a single test that takes any file in `images/` puts it through the UTK,
   and then serializes it back. 
   Fail if it differs from the original input.

- `tools/` for any and all usefully tools or scripts doing something useful with UTK.
   This would be the place to implement tools like the UEFITools extract patch and replace, 


- `UtkBase/` Implementation of all the normal UEFI elements and functionality.
   AMD, Intel and other OEMs specific shenanigans belong into different not yet created places.


- `.gitignore` Main ignore file for git


- `REAMDE.md` The file you are currently reading.


`UtkBase` contains python code split into at least two noteworthy responsibilities.

### Factories 

- Take input that a specific type of object is expected at (right at the start of the binary).
- Make the decision which object version or variance to build.
- If possible: Limit the given intput (possibly binary) for the objects' construction.
- Pass further info and steps to the object-class for construction.
- If possible: Catch errors and fall back to a more generic object variance.

Decision-making usually happens through checking specific values, offsets or building a Header object first.
The header can then be passed to the object-class to not need to build it again.

If possible, the factory is supposed to limit the input for the objects' construction.
If the input is binary, this means discarding the additional bytes after the end of the object. 

Sometimes this is not possible, which puts the final and absolute responsibility of size-limiting onto the object.

Important question: 
Does the limited binary still contain the headers of the object?
Yes, it has to. 
Otherwise, object construction becomes even more complex needing to check whether a header was passed in or not, etc.

### Many specific objects:

- Parse and then contain given input.
- If possible: Check inpout and data validity, usually through asserts.  
- Limit themselves to their actual size / data.
- Allow serialization back to the input, be that binary or others.
- Offer and implement behavior for proper manipulation or alteration.


