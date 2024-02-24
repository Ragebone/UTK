

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
