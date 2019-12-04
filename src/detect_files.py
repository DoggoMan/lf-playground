# module imports
import os

# file imports
import constants

raw_path = constants.RAW_DATA_PATH
parsed_path = constants.PARSED_DATA_PATH

# should be run from root of the project, not /src
print("### Starting from %s ###" % os.getcwd())


def printd(prefix, text):
    print("%s %s" % (prefix, text))


def scan_rawfiles():
    matches = []
    printd("1. ", "Searching path %s" % raw_path)
    printd("1.1", "Target directory contains folders %s" %
           os.listdir(raw_path))
    printd("1.2", "Scanning for raw game files...")
    for root, dirs, files in os.walk(raw_path):
        printd("1.3", "~ Searching folder %s" % root)
        for fn in files:
            if '.tdf' in fn:
                printd("1.4", "  found game: %s" % fn)
                matches.append(fn)

    print("Found %s games to parse \n" % len(matches))


def scan_parsediles():
    matches = []
    printd("1. ", "Searching path %s" % parsed_path)
    printd("1.1", "Target directory contains folders %s " %
           os.listdir(parsed_path))
    printd("1.2", "Scanning for parsed game files...")
    for root, dirs, files in os.walk(parsed_path):
        printd("1.3", "~ Searching folder %s" % root)
        for fn in files:
            if '.tdf' in fn:
                printd("1.4", "  found game: %s" % fn)
                matches.append(fn)

    print("Found %s games already parsed \n" % len(matches))


scan_rawfiles()
scan_parsediles()
