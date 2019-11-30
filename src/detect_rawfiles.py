# module imports
import os

# file imports
import constants

raw_path = constants.RAW_DATA_PATH

# should be run from root of the project, not /src
print("Running from ", os.getcwd())

print("Searching path", raw_path)
print("Target directory contains folders", os.listdir(raw_path))

matches = []

print("Scanning for game files...")
for root, dirs, files in os.walk(raw_path):
    print("~ Searching folder %s" % root)
    for fn in files:
        if '.tdf' in fn:
            print("+  found game: %s" % fn)
            matches.append(fn)

print("Found %s files to parse" % len(matches))
