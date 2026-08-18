from UtkBase.images.imageElement import ImageElement


class Firmware(ImageElement):
    """
    Interface for all UtkAmd firmware related things.
    Anything referenced in the PSP directory structures that is not a directory itself.
    """
    pass


# TODO there might have been at one point been a TypedFirmware class / interface.
# This was or might be useful to distinguish un-typed PSP Firmware blobs from ones with a Type.
# Maybe there are no un-typed firmwares though, that would explain its lack of existence