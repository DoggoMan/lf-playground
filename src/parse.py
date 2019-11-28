import functions
import pandas as pd
import numpy as np
# from functions import 'read_file_data'

filename = "1216 - Space Marines 5.tdf"
filepath = "./data/"

data = functions.read_data_file(filename, filepath)
lined = functions.get_lines(data)
lined = list(filter(None, lined))
# print(lined)

data_only = []
headers_only = []
for line in lined:
    line_type = functions.get_line_type(line)
    line_parts = functions.get_line_parts(line)
    # print(line_type, line_parts)
    if line_type == "data":
        data_only.append(line_parts)
    else:
        headers_only.append(line_parts)

headers_only.sort()
# data_only.sort()

# [print(header, '\n') for header in headers_only]
# [print(data, '\n') for data in data_only]

# df = pd.DataFrame(headers_only)

frames = []
frame_labels = []

print("headers: ", len(headers_only))
print("data: ", len(data_only))

for header in headers_only:
    header_index = header[0][1]
    label = header[0][3:]
    columns = header[1:]
    rows = list(filter(lambda l: l[0][0] == header_index, data_only))
    # print("section {} {}: [{}] {}".format(
    # header_index, label, len(rows), columns))

    if label == "event":
        data = [functions.collapse_event_line(row) for row in rows]
    else:
        data = [row[1:] for row in rows]

    # print(data)

    df = pd.DataFrame(
        data=data,
        # index=[label, ],
        columns=columns,
    )
    # print(df.iloc[0])

    frames.append(df)
    frame_labels.append(label)

print("%s sections: " % len(frames))

for i in range(0, len(frames)):
    pass
    print(" %i: %s -- %s" % (i, frame_labels[i], frames[i].shape))

# sections = functions.get_data_sections(data)
