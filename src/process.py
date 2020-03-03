
import os

import constants
import functions
import chart_score

process_bulk = True

# filepath = ""
filepath = "20191118"
# filepath = "20191125"
# filepath = "20191202"

if process_bulk:
    path = os.path.join(
        constants.RAW_DATA_PATH, str(filepath))

    files = os.listdir(path)
    files = [file for file in files if ".tdf" in file]
    print("located %s game files in path %s" % (len(files), path))
    print(files)

    for fn in files:
        pass
        # chart_score.chart_score(fn, functions.make_full_file_path(filepath), save_file=True, show_plot=False)
