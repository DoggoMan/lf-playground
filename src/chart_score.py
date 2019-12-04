# module imports
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.ndimage.filters import gaussian_filter1d

# file imports
import constants
import event_types
import functions
import parse_rawfile
import position_types

# use these two variables to target games with specific dates and game IDs
this_filename = 2047
this_filepath = 20191202

# concat the template and specific variables together
filename = "%s%s" % (this_filename, constants.base_filename)
filepath = "%s%s" % (constants.RAW_DATA_PATH, this_filepath)

pd.set_option('display.max_rows', 50)

(data, labels) = parse_rawfile.read_and_return_sections(filename, filepath)
# print(labels)

players = data[2][data[2]['type'].str.contains(
    'player')].sort_values(['team', 'category'])

print(players)

# players = [(index, row) for index, row in data[2].iterrows() if row['position']
#            != 'Referee' and row['position'] != 'Field']
print("~ identified %s players from %s entity-start's" %
      (len(players), len(data[2])))

# fig, subplots = plt.subplots(len(data[2]), 1)
# fig = plt.subplots(1, 1)

fig = plt.figure()
ax = fig.add_subplot(111)
# ax.set(xlim=(0, 1000*60*15), ylim=(0, 10000))
# ax.set_color_cycle(['red', 'green', 'blue', 'yellow'])

for index, row in players.iterrows():
    # if index > 5:
        # continue
    player_name = row['desc']
    player_team = data[1][data[1]['index'] == row['team']]['desc']
    player_team_str = player_team.tolist()[0].split(' ')[0]

    # retrieve all events relating to this player
    events = data[3][data[3]['varies'].str.contains(row['id'])]
    score_events = data[4][data[4]['entity'].str.contains(row['id'])]
    score_events = score_events.sort_values('time')

    print("%s score events for player %s" % (len(score_events), player_name))

    # vibrancy_list = ['f', 'e', 'd', 'c', 'b', 'a']
    vibrancy_list = ['', 'ff0000', 'ee0000', 'dd2200', 'aa0000', '990000']
    linestyle_list = ['-', '-.', '--', ':']

    pos_index = int(position_types.POSITION_TYPES_REVERSE[row['position']])
    color = '#' + vibrancy_list[pos_index] if player_team_str == 'Ice' else '#' + \
        vibrancy_list[pos_index][::-1]
    linestyle = linestyle_list[int(pos_index / 2)]

    # print(color, pos_index)

    x = [0, *[int(xi) for xi in score_events['time']]]
    y = [8, *[int(xi) for xi in score_events['new']]]
    # y_smoothed = gaussian_filter1d(y, sigma=2)
    y_smoothed = y

    # last_score = (x[-1], y[-1])

    ax.plot(x, y_smoothed, color=color, linestyle=linestyle, label="%s - %s %s" %
            (player_name, player_team_str, row['position']))

print('Rendering graphs...')

maxx = 1000*60*15
maxy = 10000
xticks = np.arange(0, maxx+1, step=60000)
yticks = np.arange(0, maxy+1, step=1000)

ax.legend()
ax.set(xlim=(0, maxx), ylim=(-1000, maxy))
ax.grid()

# plt.margins(x=0, y=0)
plt.xticks(xticks, [functions.millis_to_msr(xval, 'human') for xval in xticks])
plt.yticks(yticks)
plt.show()
