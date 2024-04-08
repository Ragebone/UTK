import csv


class GuidDatabase:
    """
    A class to manage known UEFI GUIDs and their known or assumed names
    """

    _database = {}

    @staticmethod
    def getDatabase():
        """
        Use for manually altering the database yourself
        :return: The dictionary that is the database; Mapping GUID-string to a name.
        """
        return GuidDatabase._database

    @staticmethod
    def getNameFromGuidString(guidString: str, defaultString: str = "") -> str:
        """
        Retrieve a possible name for and by its GUID string from the database

        :param guidString: The UEFI GUID toString()ed
        :param defaultString: Optional, default "", what should be returned if the GUID string is not contained in the database
        :return: The name as a String
        """
        return GuidDatabase._database.get(guidString, defaultString)

    @staticmethod
    def fromCsvFile(filename):
        """
        Load a csv file into the database dictionary
        :param filename: Path to the csv file
        :return: The dictionary; this can be ignored. Use GuidDatabase.getNameFromGuidString(...) unless you have reasons not to.
        """

        guidDict = GuidDatabase._database
        with open(filename) as csvfile:
            guids = csv.reader(csvfile, quoting=csv.QUOTE_NONE)

            for row in guids:
                guidString = row[0].strip()
                name = row[1].strip()
                previousName = guidDict.get(guidString, None)
                if previousName is not None:
                    name += " | {}".format(previousName)
                guidDict[guidString] = name

        GuidDatabase._database = guidDict
        return guidDict
