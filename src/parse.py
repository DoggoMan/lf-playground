import functions
import pandas as pd
import numpy as np
# from functions import 'read_file_data'

filename = "1216 - Space Marines 5.tdf"
filepath = "./data/"

raw_data = functions.read_data_file(filename, filepath)

cleaned_data = functions.remove_spacing(raw_data)
lined = functions.get_lines(cleaned_data)
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

# print(headers_only)
# print(data_only)
[print(header) for header in headers_only]
[print(data) for data in data_only]

df = pd.DataFrame(headers_only)

frames = []
frame_labels = []

print("headers: ", len(headers_only))
print("data: ", len(data_only))

for header in headers_only:
    header_index = header[0][1]
    label = header[0][3:]
    columns = header[1:]
    lines = list(filter(lambda l: l[0][0] == header_index, data_only))
    print("{} {}: {} lines \n {}".format(
        header_index, label, len(lines), columns))

    if label == "event":
        data = [functions.collapse_event_line(line) for line in lines]
    else:
        data = [line[1:] for line in lines]

    print(data)

    df = pd.DataFrame(
        data=data,
        # index=[label, ],
        columns=columns,
    )

    frames.append(df)
    frame_labels.append(label)

for i in range(0, len(frames)):
    print("\n", frame_labels[i])
    print(frames[i])

sections = functions.get_data_sections(raw_data)
