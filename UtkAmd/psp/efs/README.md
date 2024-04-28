# EFS: Embedded Firmware Structure

Called the Firmware Entry Table or FET for short in the PSPTool.

It is a structure starting with a signature of 0xAA55AA55,
and it mainly consists pointers at other firmware and directory structures.
The PSP uses it to search for its specific directories and firmware.

## Numerous problems with the EFS in UTK

There seems to be no clear indicating which version the EFS is and hence,
which generation of CPUs the EFS supports.

Currently, there is only one implementation for an EFS,
the [ZenEfs](./zenEfs.py) in the hopes that no serious issues arise from only having one implementation.

The main reference for this implementation is in 
[eigenform's ragesa](https://github.com/eigenform/ragesa/blob/main/src/efs.rs).

It was chosen for being the most `complete` one with various additional references and values compared to many others.

Not all those values are clear on their meaning and usage.

And there are references like the `Promontory` reference to unknown firmware blobs of unclear size.
With `Promontory` specifically naming the FCH / PCH on X570 and beyond.
It is hence to be expected that systems without those specific chipsets do not have or feature such references in their EFS. 

Pragmatically, the only platforms that could guarantee all CPUs looking for such EFS references would be AM5 and SP5.
Because the `Promontory` FCH wasn't a thing with `Zen1`.

## Other references and EFS implementations

- [Coreboot PSP_integration](https://github.com/coreboot/coreboot/blob/master/Documentation/soc/amd/psp_integration.md)
- [PSPTool]()
- [OpenSIL AGCL-R]