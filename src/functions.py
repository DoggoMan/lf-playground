# module imports
import re
import os
import json

# file imports
import constants

def make_full_file_path(path):
    return "%s%s" % (constants.RAW_DATA_PATH, path)

def make_full_file_name(name):
    return "%s%s" % (name, constants.base_filename)

def read_data_file(name, path):
    f = open(os.path.join(path, name),
             "r", encoding='utf-16-le')
    raw = f.read()
    f.close()

    print("Read data from file '{}', got {} bytes".format(name, len(raw)))
    return raw


def write_parsed_file(filename, parsed_data: object):
    write_path = os.path.join(constants.PARSED_DATA_PATH, filename)
    json.dump(parsed_data, write_path)
    return True


def get_lines(text):
    lined = text.split("\n")
    return list(map(str.strip, lined))
    # return lined


def get_line_parts(line):
    parts = line.split("\t")
    return parts


def collapse_event_line(event_line):
    # subtype = get_event_subtype(event_line)
    time = event_line[1]
    type = event_line[2]
    varies = ' '.join(event_line[3:])
    time_str = millis_to_msr(time, 'human')

    initiator = event_line[3] if len(event_line) > 3 else ''
    activity = event_line[4] if len(event_line) > 4 else ''
    target = event_line[5] if len(event_line) > 5 else ''

    return [time, type, varies, initiator, activity, target, time_str]


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


def get_headers(raw_data):
    pass


def get_data(raw_data):
    pass


"""
Helper function to convert a raw milliseconds integer to 
minutes, seconds, and remaining millis
"""


def millis_to_msr(millis, format='raw'):
    millis = int(millis)
    seconds = (millis/1000) % 60
    seconds = int(seconds)
    minutes = (millis/(1000*60)) % 60
    minutes = int(minutes)

    if format == 'raw':
        return (minutes, seconds, millis % 1000)
    elif format == 'human':
        return f"{minutes:02d}:{seconds:02d}"
        # return f"{minutes:02d}:{seconds:02d}:{millis%1000:04d}"
    else:
        return (minutes, seconds, millis % 1000)
