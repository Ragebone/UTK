# Universal firmware Tool Kit

An object-oriented package, framework and collection of tools for and around firmware like UEFI images and bios files. 

Heavily influenced by the famous [UEFITool by LongSoft](https://github.com/LongSoft/UEFITool "UEFITool Github repo") and
[PSPTool by PSPReverse](https://github.com/PSPReverse/PSPTool "PSPTool Github repo") as well as [uefi-firmware-parser](https://github.com/theopolis/uefi-firmware-parser "Github repo").


## Usage

The overall usability is pretty limited at this point.
If human-readable names for UEFI GUIDs are wanted, simply add a `uefiGuids.csv` file to your working directory.
The one from the UEFITool repository is pretty good and recommended.

On the code side, the main starting-point currently is the `BiosFile`.
It is meant to take a firmware file as is delivered by a motherboards' manufacturer.
In this example with a `Asus WRX80 sage` capsule file.

```python
from UtkBase.biosFile import BiosFile

bios = BiosFile.fromFilepath("./Pro-WS-WRX80E-SAGE-SE-WIFI-ASUS-1003.CAP")
```

From then on, usage should (hopefully) be straight forward.

In the future, the `wiki` is the place to go for more documentation on how to use UTK.

## Further Links

[The motivation behind this project](./motivation.md)
[The roadmap and where this goes in the future](./roadmap.md)
[Ruminations on the software-architecture](./architecture.md)

## References to look into 

https://github.com/galkinvv/amdmeminfo
https://github.com/galkinvv/galkinvv.github.io/blob/master/block_err_test.py
https://github.com/galkinvv/galkinvv.github.io/blob/master/direct-mem-test.py
https://github.com/galkinvv/pcie_mem_test
https://github.com/galkinvv/PolarisBiosEditor-xml
https://github.com/galkinvv/pwndbg
https://github.com/platomav/BIOSUtilities
https://firmwaresecurity.com/2018/10/30/ami-bios-guard-extractor-parses-ami-bios-guard-a-k-a-pfat-images-and-extracts-a-proper-spi-bios-image/
https://github.com/IOActive/Platbox/tree/df1e21bbea1a9b1ac7777143a3affdeb8c609c55
specifically: https://github.com/IOActive/Platbox/blob/df1e21bbea1a9b1ac7777143a3affdeb8c609c55/tools/efs_parser.py

https://github.com/nstarke/utk-web/tree/70949997815049e31ce7672391854716b2070031

really really look here:
https://github.com/linuxboot/fiano/tree/0ad88a5434e67ab30e2851873a33c7208cfa2db8/pkg/amd

really really really look at the EDK2 source for stuff
https://github.com/tianocore/edk2-platforms/blob/b64443f7b8c37b90e04e08bb8dd0ce48fa602580/Platform/AMD/VanGoghBoard/AgesaPublic/Include/Library/AmdPspBaseLibV2.h#L22

https://github.com/Mimoja/amdfw/blob/2218359ecbdcbb1bed26e16521a213107a0dd68f/directory.go#L12

https://github.com/openSIL/AGCL-R/tree/0a60473007604550bd0fb708cc1a820240d1bc51
https://github.com/openSIL/AGCL-R/blob/0a60473007604550bd0fb708cc1a820240d1bc51/AgesaPkg/Addendum/GenoaSp5Rdimm/Apcb/GenoaSp5Rdimm/ApcbCreate.py