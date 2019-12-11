# module imports
import pandas as pd

# file imports
import position_types
import functions

pd.set_option('display.max_rows', 100)


def read_and_return_sections(filename, filepath, verbose=False):
    def vprint(*args):
        if verbose:
            print(*args)
        else:
            pass

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

    vprint("headers: ", len(headers_only))
    vprint("data: ", len(data_only))

    for header in headers_only:
        header_index = header[0][1]
        label = header[0][3:]
        rows = list(filter(lambda l: l[0][0] == header_index, data_only))
        # print("section {} {}: [{}] {}".format(
        # header_index, label, len(rows), columns))

        columns = []
        data = []
        if label == "event":
            columns = [*header[1:], 'initiator',
                       'activity', 'target', 'time_str']
            data = [functions.collapse_event_line(row) for row in rows]
        elif label == "entity-start":
            columns = [*header[1:], 'position']
            data = [[*row[1:], 'Referee' if row[3] == 'referee' else position_types.POSITION_TYPES[row[-1]]]
                    for row in rows]
        else:
            columns = header[1:]
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

    vprint("%s sections: " % len(frames))

    for i in range(0, len(frames)):
        pass
        vprint(" %i: %s -- %s" % (i, frame_labels[i], frames[i].shape))
        vprint("  ", list(frames[i].columns))

    return (frames, frame_labels)
