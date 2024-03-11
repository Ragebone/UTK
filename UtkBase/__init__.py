import traceback

from UtkBase.guidDatabase import GuidDatabase

#
# CSVs can for instance be had from the UEFITool repository.
# Place the aptly named csv inside your working directory,
# or change the path to an absolute one.
#

try:
    GuidDatabase.fromCsvFile("./uefiGuids.csv")         # Working directory
except Exception as ex:
    # Catch all exceptions because UTK doesn't really care about readable GUID names
    traceback.print_exception(type(ex), ex, ex.__traceback__)
