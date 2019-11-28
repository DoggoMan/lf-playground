import functions
import parse
import event_types
import pandas as pd

base_filename = " - Space Marines 5.tdf"
base_filepath = "./data/raw/"

this_filename = "%s%s" % (2004, base_filename)
this_filepath = "%s%s" % (base_filepath, 20191125)

# filename = "1216 - Space Marines 5.tdf"
# filepath = "./data/test/"
# filename = "2004 - Space Marines 5.tdf"
# filepath = "./data/raw/20191125"

# pd.set_option('display.max_rows', 10)

(data, labels) = parse.read_and_return_sections(this_filename, this_filepath)
print(labels)

print(data[2])
print('\n')
for index, row in data[2].iterrows():
    # skip non-players
    if row['position'] == 'Referee' or row['position'] == 'Field':
        continue

    # retrieves all events relating to this player
    events = [e for e_index, e in data[3].iterrows() if row['id']
              in e['varies']]
    self_events = [e for e_index, e in data[3].iterrows() if
                   e['varies'].find(row['id']) == 0]
    print("[%s / %s] \t%s" % (len(self_events), len(events), row['desc']))

    