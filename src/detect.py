import os

base_path = "./data/"
raw_path = os.path.join(base_path, "raw/")


print("Starting from ", os.getcwd())
print("Base directory contains", os.listdir(base_path))
print("Searching path", raw_path)
print("Target directory contains", os.listdir(raw_path))

matches = []

print("Scanning for game files...")
for root, dirs, files in os.walk(raw_path):
    for fn in files:
        if '.tdf' in fn:
            print(" found game: %s" % fn)
            matches.append(fn)

print("Found %s files to parse" % len(matches))
