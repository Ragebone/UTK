import argparse
import json
import logging


from UtkBase.biosFile import BiosFile
from tools.common.conversions import convertItem
from tools.common.loggerSettings import applyLogSettings, addLoggingFlags


def main():
    """
    UTK Info main function

    :return:
    """
    argParser = argparse.ArgumentParser(
        prog="UTK Info",
        description='Print everything known about the given BiosFile(s)\nOutput format is JSON',
        epilog="Use -h or --help for more information"
    )
    # Application default Arguments
    addLoggingFlags(argParser)

    argParser.add_argument('filenames', metavar='F', type=str, nargs='+', help='File / Path Bios file')

    # NOTE current default output is JSON ...
    # argParser.add_argument("-j", "--json", required=False, action='store_true', help="Sets the output format to json")
    # argParser.add_argument("-t", "--text", required=False, action='store_true', help="Sets the output format to json")

    arguments = vars(argParser.parse_args())

    applyLogSettings(arguments)

    filePaths = arguments.get("filenames")
    for path in filePaths:

        # NOTE uncomment when debugging to halt on exceptions
        # BiosFile.disableExceptionHandling()

        try:
            bios = BiosFile.fromFilepath(path)
        except Exception as ex:
            if BiosFile.dontHandleExceptions:
                raise ex
            logging.error(ex.__traceback__)
            print("\n\nFailed building BiosFile from:\n{}\nPossible reason:\n{}".format(path, ex))
            continue

        print("{}\n".format(path))
        biosDict = convertItem(bios, 0xFF)
        string = json.dumps(biosDict, indent=4)
        print(string)


if __name__ == "__main__":
    main()
