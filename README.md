# Universal firmware Tool Kit

An object-oriented package, framework and collection of tools for and around firmware like UEFI images and bios files. 

Heavily influenced by the famous [UEFITool by LongSoft](https://github.com/LongSoft/UEFITool "UEFITool Github repo") and [PSPTool by PSPReverse](https://github.com/PSPReverse/PSPTool "PSPTool Github repo").
Noteworthy as well: [uefi-firmware-parser](https://github.com/theopolis/uefi-firmware-parser "Github repo")


## Usage

The overall usability is pretty limited at this point.
If human-readable names for UEFI GUIDs is wanted, simply add a `uefiGuids.csv` file to your working directory.
The one from the UEFITool repository is pretty good and recommended.

On the code side, the main starting-point currently is the `BiosFile`.
It is meant to take a firmware file as is delivered by a motherboards' manufacturer.
In this example with a `Asus WRX80 sage` capsule file.

```python
from UtkBase.biosFile import BiosFile

bios = BiosFile.fromFilepath("./Pro-WS-WRX80E-SAGE-SE-WIFI-ASUS-1003.CAP")
```

From then on, usage should (hopefully) be straight forward.

## Roadmap

In no particular order

- [x] Initial shallow implementation down to the UEFI volume level 
- [x] Rough implementation down to UEFI files and sections, even compressed ones
- [x] Basic-ish documentation in README.md files
- [x] UEFI GUID database and name support
- [x] Intermediate format; Python Dictionaries with `toDict(self) -> dict[str, Any]`
- [x] ~~Intermediate format JSON serialization via toJson() methods~~
- [ ] Full UEFI implementation on par with UEFITool
      - Some parts are still horrible
      - More Capsule-Headers need supporting 
  - Fully understand, parse and use those headers
      - More Volumes, file-systems, and other specifics are still needed
- [ ] Full implementation down to decompression and compression
      - Blocked by proper compression of LZMA compressed Sections
        Compressing is easy, but does it work still work?
        the new compressed binary is completely different to the previous one.
        That breaks the tests at minimum.

- [ ] Proper Capsule handling with an interface and multiple Classes for the different capsules and then sub structures

- [ ] (Flash) Offset remembering and pass through in fromBinary() 
- [ ] GUID management framework
- [ ] Strings search in framework
- [ ] Deterministic export to and import from a directory structure
- [ ] Implement UEFI checksum calculations and verification
  - [x] Implement UEFI volume-header crc16 calculations
    - [ ] TODO: proper "verification" functionality 
    
- [ ] Crypto system for signature management, verification and signing
- [ ] AMD flavored firmware handling
  - [ ] AMD PSP EFS detection and construction
  - [ ] AMD PSP directories
  - [ ] AMD PSP firmware
  - [ ] AMD PSP structure manipulation and rebuilding
  - [ ] AMD PSP firmware signature verification
  - [ ] AMD PSP firmware signature resigning

- [ ] Intel flavored firmware handling
- [ ] HII capability
- [ ] PCD capability
- [ ] NVAR Capability
- [ ] Address and referencing framework  References is what it is gona be called, probably
- [ ] Support for emulation and further automation
- [ ] Package release for easy usage
- [ ] Support advanced firmware analysis
- [ ] Integrate with QEMU
- [ ] Integrate with other tools
- [ ] Integrate with EMBA
- [ ] Support emulation
- [ ] Support proxy execution and debugging
- [ ] Actual tools and use-cases
  - Info printing;   tools/info.py  something like the report generated by the UEFITools UEFIExtract -r
  - Extract everything to directories
  - Extract something specific
  - Rebuild 
  - Replace something(s) by its GUID
  - Unlocking hidden bios options
    - Unlocking AMD CBS for instance
  - Adding new settings / menus to the UEFI user interface
  - Changing default bios settings
  - 
  - Others? 

### Roadmap-ed use-cases 

One still open question here is how to properly use those pieces of python code.

To envision a few possibilities:

#### Get me what ever is at offset 0x21000

```python
from UtkBase.biosFile import BiosFile
bios = BiosFile.fromFilepath("./Pro-WS-WRX80E-SAGE-SE-WIFI-ASUS-1003.CAP")

objectAtOffset = bios.getObjectAt(0x21000)
```

In this specific showcase, the object should be an AMD specific structure that isn't implemented yet.
Neither is the functionality to get something at an offset.
To add to this idea, the offset should result in the same object as long as the object is the smallest known thing at location. 
And as long as the offset is within the objects bounds.

#### Batch replacements by GUID and from a reference

This would need to be implemented as a separate tool in `tools/`.
But once there is a list of objects that have UefiGuids, it could look like this:

```python
from UtkBase.biosFile import BiosFile
bios = BiosFile.fromFilepath("./Pro-WS-WRX80E-SAGE-SE-WIFI-ASUS-1003.CAP")
listOfThingsToReplace = ['objects that have GUIDs, pulled from another Bios / image']
bios.replace(listOfThingsToReplace)
```

Maybe instead of a list, have it be a dictionary that directly maps GUID strings to the object to be replaced.

#### Insert, Add, Remove things

Inserting, adding and removing something, anything really, is the obvious and most relevant use-case.
One important decision already is to not expose the datastructures for manual alterations like that.
That is because checksums and others details might need to be adjusted in order to nor break the firmware.
Instead, fitting methods need to handle such details when altering.

## Architecture

Each folder attempts to contain only what the respective UEFI thing is made out of.

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

- Parse the given binary intput;  `.fromBinary()` method.
- Construct object from the inpout; `__init__` done in the constructor.
- If possible: Check inpout and data validity, usually through asserts.  
- Limit themselves to their actual size / data.
- Allow serialization back to the input, be that binary or others.
- Offer and implement behavior for proper manipulation or alteration.

Of note is that the constructor of an object takes the specific values.
The `uefi-firmware-parser` for instance just takes the binary "data" in the constructor.
The binary gets handled by the class or static methods fromBinary() specifically.
One thought behind this is that this should allow easy manual creation of objects.
No clear reasonable use-case exists for this yet, but maybe that changes in the future. 
An additional thought; Objects could / should default to sensible default values of their attributes.
Everything to ease creation and usage.

