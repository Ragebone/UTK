

class Child:
    """
    Implementation of Child functionality for anything that has a parent object somewhere

    """

    def __init__(self):
        self._parent = None

    def setParent(self, parent):
        """

        :param parent:
        :return:
        """
        self._parent = parent

    def getParent(self):
        """

        :return:
        """
        return self._parent
