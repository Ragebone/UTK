import abc


class BuildZenImage:

    @abc.abstractmethod
    def buildPspFirmwareStructures(self):
        """

        :return:
        """
        pass


class BottomUp(BuildZenImage):
    """



    """

    def buildPspFirmwareStructures(self):
        pass


class TopDown(BuildZenImage):
    """


    """

    def buildPspFirmwareStructures(self):
        pass


