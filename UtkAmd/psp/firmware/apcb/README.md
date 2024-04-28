# APCB

Everything on and for the AGESA PSP Customization Block (APCB) and its UTK specific implementation. 


## Structure

APCBs contain groups which contain types which can then contain very specific information. 

``` 
APCB -> Group -> Type -> Data?
```

One thing Types can contain are `Tokens`, simple key value pairs.
Keys and their meanings have not been clear and public knowledge in the past.

[A comprehensive list of APCB V3 Tokens](https://github.com/openSIL/AGCL-R/blob/0a60473007604550bd0fb708cc1a820240d1bc51/AgesaPkg/Addendum/GenoaSp5Rdimm/Apcb/Inc/Genoa/ApcbV3TokenUid.h)

## Cool related projects or usecases

Some people seem to be modifying their ASUS ROG Ally handheld gaming devices with more memory.
[APCB_ROG_Ally APCB modifications needed](https://github.com/95JakeHex/APCB_ROG_Ally?tab=readme-ov-file).

## References

There have been multiple versions of APCBs and tools for parsing and working with APCBs in the past.

A non-exhaustive list of projects in no particular order:

- [Tim-- python3 based apcbtool](https://github.com/Tim---/apcbtool/tree/main)
- [Oxidecomputer rust amd-apcb](https://github.com/oxidecomputer/amd-apcb)
- [Coreboot apbc utilities](https://github.com/system76/coreboot/tree/6a6f7f8db01a366c98246f5847f58a266d0f7f10/util/apcb)

Though most notably is the [OpenSIL AGCL-R Repository](https://github.com/openSIL/AGCL-R) published in approximately January 2024.

It features the [ApcbCreate.py](https://github.com/openSIL/AGCL-R/blob/0a60473007604550bd0fb708cc1a820240d1bc51/AgesaPkg/Addendum/GenoaSp5Rdimm/Apcb/GenoaSp5Rdimm/ApcbCreate.py)
to built APCBs from their source definition.
