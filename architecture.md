# Architecture

Each folder attempts to contain only what the respective UEFI thing is made out of.

What ever the UEFI thing contains, is then supposed to be in a subdirectory hopefully aptly named.

README.md documents in each directory are supposed to contain further information. 

The current directory structure:

```
UTK
├── images/
├── tests/
├── tools/
├── UtkAmd/
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
   This would be the place to implement tools like the UEFITools extract patch and replace 


- `UtkAmd/` Directory for all AMD specific implementations.


- `UtkBase/` Implementation of all the normal UEFI elements and functionality.
   AMD, Intel and other OEMs specific shenanigans belong into different not yet created places.
   `TODO maybe rename to UtkUefi since it contains the basic uefi building blocks`


- `.gitignore` Main ignore file for git


- `REAMDE.md` The file you are currently reading.


`Utk****` contain at least two noteworthy responsibilities.


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

