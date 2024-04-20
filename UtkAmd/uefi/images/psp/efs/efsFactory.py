from UtkAmd.uefi.images.psp.efs.zenEfs import ZenEfs


class EfsFactory:

    @staticmethod
    def fromBinary(binary: bytes, offset: int = None):

        # TODO proper EFS checking.
        efs = ZenEfs.fromBinary(binary, offset)
        return efs
