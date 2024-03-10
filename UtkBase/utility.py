

def binaryIsEmpty(binary: bytes) -> bool:
    """
    True if binary consists only of 0xFF ...
    :param binary: The bytes to check
    :return: Bool
    """
    for byte in binary:
        if byte != 0xFF:
            return False

    return True


def diffBinary(binA: bytes, binB: bytes) -> bool:
    """
    byte wise compare binaries. True if equal
    :param binA:
    :param binB:
    :return:
    """
    equals = True
    offset = 0
    while offset < len(binA) and offset < len(binB):
        a = binA[offset]
        b = binB[offset]

        offset += 1

        if a == b:
            continue

        equals = False
        print("Offset: {} dec: {}\nA: {}\nB: {}\n".format(hex(offset), offset, binA[offset:offset+256], binB[offset:offset+256]))
        offset += 256

    return equals


def fillBinaryTill(binary: bytes, targetSize: int, filler: bytes = b'\xFF') -> bytes:
    """
    Fills the given binary with a filler-value until it is as large as the target-size.

    Useful for creating paddings between things.
    The Padding or Filler value defaults to 0xFF but can be optionally set to what ever is desired.
    0xFF and 0x00 make the most sense as the filler-value.

    :param binary: Binary to add filler / padding to
    :param targetSize: Size of the Binary to fill it up to
    :param filler: A single byte to be repeatedly added to the given binary. 0xFF and 0x00 make the most sense. By default, b'\xFF'.
    :return: Binary of the target-size
    """
    amountOfFiller = targetSize - len(binary)
    assert amountOfFiller >= 0, "Binary larger then requested Size of {}, actual size {}\n Can't shrink the Binary here".format(hex(targetSize), hex(len(binary)))
    if 0 == amountOfFiller:
        return binary
    fillerBin = amountOfFiller * filler
    binary += fillerBin
    return binary


def alignOffset(offset: int, alignment: int) -> int:
    """
    Align the offset with the given alignment

    Use for Offset and padding calculations when there are specific alignment requirements like block-sizes.

    :param offset: offset to be aligned
    :param alignment: Alignment-Number to align the offset with
    :return: the new offset after alignment
    """
    alignedOffset = offset + ((alignment - (offset & (alignment - 1))) & (alignment - 1))
    return alignedOffset


def alignOffsetDown(offset: int, alignment: int) -> int:
    """
    Align the offset 'down' to a smaller number with the given alignment

    Use this for example when building binaries from the back to the front.

    :param offset: offset to be aligned
    :param alignment: Alignment-Number to align the offset with
    :return: the new offset after alignment
    """
    mask = alignment - 1
    invertedMask = mask.__invert__()
    newAddress = offset & invertedMask
    return newAddress
