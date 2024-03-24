# Encapsulation of UEFI images | Capsules

Many OEMs don't just deliver a raw binary as firmware for their Motherboards.

Asus for instance nowadays uses `.CAP` file formats, hinting at the usa of encapsulation.

Put simply, the actual UEFI firmware is preceded by something else.
Some sort of structure and information used in the firmware update procedure.

Some of those structures are known, others only partially or not at all.

