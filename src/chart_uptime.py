# module imports
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# file imports
import constants
import event_types
import functions
import parse_rawfile

# use these two variables to target games with specific dates and game IDs
this_filename = 2004
this_filepath = 20191125

# easy constant for manipulating number of plots returned
max_graphs = 5

# concat the template and specific variables together
filename = "%s%s" % (this_filename, constants.base_filename)
filepath = "%s%s" % (constants.RAW_DATA_PATH, this_filepath)

pd.set_option('display.max_rows', 50)

(data, labels) = parse_rawfile.read_and_return_sections(filename, filepath)
print(labels)

print(data[2])
print('\n')

players = [(index, row) for index, row in data[2].iterrows() if row['position']
           != 'Referee' and row['position'] != 'Field']
print("identified %s players from %s entity-start's" %
      (len(players), len(data[2])))

# fig, subplots = plt.subplots(len(data[2]), 1)
fig, subplots = plt.subplots(max_graphs, 1)
graph_i = 0

# for index, row in data[2].iterrows():
for index, row in players:
    # skip non-players
    if row['position'] == 'Referee' or row['position'] == 'Field':
        continue

    player_team = data[1][data[1]['index'] == row['team']]['desc']
    player_team_str = player_team.tolist()[0].split(' ')[0]

    # retrieve all events relating to this player
    events = data[3][data[3]['varies'].str.contains(row['id'])]

    # events['time_str'] = events['time'].apply(
    #     lambda x: functions.millis_to_msr(x, 'human'))

    self_events = data[3][data[3]['initiator'].str.contains(row['id'])]
    else_events = data[3][data[3]['target'].str.contains(row['id'])]

    deac_types = [
        "0206",
        "0306",
        # enemy nuke?? not sure how to find these easily
    ]

    self_deacs = else_events[else_events['type'].isin(deac_types)]
    enemy_deacs = self_events[self_events['type'].isin(deac_types)]

    print("[%s / %s] \t%s" % (len(self_events), len(events), row['desc']))

    if graph_i < max_graphs:
        # print(events[['varies']])
        # print(self_deacs)
        print(f"Creating graph #{graph_i} for player {row['desc']}")

        x = [int(deac['time']) for index, deac in self_deacs.iterrows()]
        y = np.full((len(x), 1), -1)

        x2 = [int(deac['time']) for index, deac in enemy_deacs.iterrows()]
        y2 = np.full((len(x2), 1), 1)

        # use the graph index variable
        plot = subplots[graph_i]
        graph_i = graph_i + 1

        plot.set(xlim=(0, 1000*60*15), ylim=(-3, 3))

        # plot.plot(x, y, x2, y2, color='black')
        plot.scatter(x, y, color='red', marker='o', s=2)
        plot.scatter(x2, y2, color='green', marker='o', s=2)

        plot.title.set_text('%s - %s %s' %
                            (row['desc'], player_team_str, row['position']))

    # score graph ?
    # line graph of player's score as it changed throughout the game?
    # plot.set(xlim=(0, 1000*60*15), ylim=(0, 15000))

print('Rendering graphs...')

fig.subplots_adjust(hspace=1.0)
plt.show()
