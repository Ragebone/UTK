# UTK AMD specific firmware

The PSP in AMD Zen based processors has many different blobs of firmware and other things. 
This is the place for all their different implementations.

## State of the Art

Currently, no further actions are taken with the blobs.

A generic "FirmwareBlob" implementation allows the overall handling of blobs within the image.
But it does not allow any operations on the blobs themselves. 
Operations on blobs for instance being signature verification and resigning.

## Roadmap

- [ ] support for APCBs: WORK IN PROGRESS
- [ ] support for APOBs
- [ ] Signature verification
- [ ] Re-signing
- [ ] Decompression
- [ ] Decryption
- [ ] support for emulation and further analysis
