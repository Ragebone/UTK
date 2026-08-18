from UtkAmd.psp.zenReference import ZenReference


class ReferenceMap:
    references = {}

    @staticmethod
    def handledCollision(reference: ZenReference) -> bool:
        """

        :param reference:
        :return:
        """
        OFFSET = reference.getAbsoluteOffset()
        collidingReference = ReferenceMap.references.get(hex(OFFSET))
        if collidingReference is None:
            return False

        entry = collidingReference.followReference()
        if entry is not None:
            reference.setEntry(entry)
            entry.registerReference(reference)

        return True

    @staticmethod
    def addReference(reference: ZenReference):
        map = ReferenceMap.references

        OFFSET = reference.getAbsoluteOffset()
        collision = ReferenceMap.references.get(hex(OFFSET))
        assert collision is None, "Collision with references?"

        ReferenceMap.references[hex(OFFSET)] = reference
