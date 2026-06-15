import logging


def addLoggingFlags(argParser):
    argParser.add_argument("-v", "--verbose", required=False, action='store_true', help="Verbose Output")
    argParser.add_argument("-vv", "--verboseVerbose", required=False, action='store_true', help="super Verbose Output")
    argParser.add_argument("-ulf", "--useLogFile", required=False, action='store_true', help="Enables logging to a file")


def applyLogSettings(arguments: dict):
    verbose = arguments.get("verbose", False)
    verboseVerbose = arguments.get("verboseVerbose", False)
    useLogfile = arguments.get("useLogFile", False)

    loggingLevel = logging.ERROR
    logFile = None

    if verbose:
        loggingLevel = logging.WARNING
    if verboseVerbose:
        loggingLevel = logging.INFO

    if useLogfile:
        logFile = "tool.log"

    logging.basicConfig(filename=logFile, level=loggingLevel)
