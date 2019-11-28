import re
import os


def read_data_file(name, path):
    f = open(os.path.join(path, name),
             "r", encoding='utf-16-le')
    raw = f.read()
    f.close()

    print("Read data from file '{}', got {} bytes".format(name, len(raw)))
    return raw


def get_lines(text):
    lined = text.split("\n")
    return list(map(str.strip, lined))
    # return lined


def get_line_parts(line):
    parts = line.split("\t")
    return parts


def collapse_event_line(event_line):
    subtype = get_event_subtype(event_line)
    time = event_line[1]
    type = event_line[2]
    varies = ' '.join(event_line[3:])
    return [time, type, varies]


def get_event_subtype(event_line):
    if "Mission" in event_line[-1]:
        return "mission_status"
    elif "zaps" in event_line:
        return "zap"
    elif "resupplies team" in event_line:
        return "boost"
    elif "destroys" in event_line:
        return "base_capture"
    elif "achievement" in event_line:
        return "acheivement"
    else:
        return "unknown"


def get_line_type(line):
    if len(line) < 1:
        return "?"
    if ";" in line[0]:
        return "header"
    else:
        return "data"


def get_data_sections(raw_data):
    matches = re.findall(r"^;\d+\/", raw_data)
    # print(matches)
    return matches


def get_headers(raw_data):
    pass


def get_data(raw_data):
    pass
