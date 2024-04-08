# UTK Base package 

A package for a common UEFI firmware implementation.
Tested and build for AMD Ryzen at the moment.
Intel based images will not work right now.

`TODO` This package / module could and maybe should be named `UtkUefi`,
to signify it implementing general UEFI  "things".

## Content

```
UtkBase
├── capsuleHeaders/
├── images/
├── interfaces/
├── biosFile.py
├── README.md
├── uefiGuid.py
└── utility.py
```

- `capsuleHeaders/` for all the different Encapsulations of UEFI Images.
    Files like the `.CAP` commonly used by ASUS start with a header followed by the actual Images.
    This makes the file larger than the actual EEPROM on the boards.
    This header is commonly used to verify compatibility with the system.
    As well as authenticity and other miscellaneous things like a version and date.
        

- `images/` implementations for a "generic" UEFI Image and its content. 
  The folder is called `images` to refer to the BiosFiles content.
  A BiosFile can contain multiple UEFI images, hence the name 

- `interfaces/` for common interface definitions like `serializable` for instance.

- `biosFile.py` Main entrypoint. Use with .fromFilePath(...) or fromBinary(...)

- `README.md` This file

- `uefiGuid.py` Implementation of the UEFI GUID 128-bit integers used everywhere.
    Placed here because it is used everywhere!

- `utility.py` Commonly used utility functions.
