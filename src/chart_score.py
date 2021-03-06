# module imports
import os
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

####     TODOS      ####
# :)


def chart_score(filename, filepath, show_plot=False, save_file=False, anti_smoothing=True, verbose=False):
    def vprint(*args):
        if verbose:
            print(*args)
        else:
            pass

    pd.set_option('display.max_rows', 50)

    (data, labels) = parse_rawfile.read_and_return_sections(filename, filepath, verbose)

    players = data[2][data[2]['type'].str.contains(
        'player')].sort_values(['team', 'category'])

    vprint(players)

    vprint("~ identified %s players from %s entity-start's" %
           (len(players), len(data[2])))

    fig = plt.figure(figsize=(14, 10), dpi=80, facecolor='w', edgecolor='k')
    ax = fig.add_subplot(111)
    # ax.set_color_cycle(['red', 'green', 'blue', 'yellow'])

    maxx = 1000*60*15
    xticks = np.arange(0, maxx+1, step=60000)

    # adjust maxy based on highest player score
    final_scores = data[5].astype({'score': 'int32'}).sort_values(
        'score', ascending=False)['score']
    highest_score = final_scores.head(1).values[0]
    vprint('High scores:', highest_score, final_scores)

    maxy = 10000 if int(highest_score) < 10000 else (
        int(highest_score/1000)+1) * 1000
    yticks = np.arange(0, maxy+1, step=1000)

    for index, row in players.iterrows():
        player_name = row['desc'].replace('_', '')
        player_team = data[1][data[1]['index'] == row['team']]['desc']
        player_team_str = player_team.tolist()[0].split(' ')[0]

        player_entity_end = data[5][data[5]['id'].str.contains(row['id'])]
        player_end_state = data[6][data[6]['id'].str.contains(row['id'])]
        player_survived = True if int(player_end_state['livesLeft'].tolist()[
            0]) > 0 else False

        # retrieve all events relating to this player
        events = data[3][data[3]['varies'].str.contains(row['id'])]
        score_events = data[4][data[4]['entity'].str.contains(row['id'])]
        score_events = score_events.sort_values('time')

        vprint("%s score events for player %s" %
               (len(score_events), player_name))
        vprint("player %s %s" %
               (player_name, 'Survived' if player_survived else 'Died'))

        # vibrancy_list = ['f', 'e', 'd', 'c', 'b', 'a']
        vibrancy_list = ['', 'ff0000', 'ee0000', 'dd8800', 'dd8800', '880000']
        linestyle_list = ['', '-', '--', '--', '--', ':']

        pos_index = int(position_types.POSITION_TYPES_REVERSE[row['position']])
        color = '#' + vibrancy_list[pos_index] if player_team_str == 'Fire' else '#' + \
            vibrancy_list[pos_index][::-1]
        linestyle = linestyle_list[int(pos_index)]

        # vprint(color, pos_index)

        x = [0, *[int(xi) for xi in score_events['time']]]
        y = [0, *[int(xi) for xi in score_events['new']]]
        # y = gaussian_filter1d(y, sigma=2)

        end = int(player_entity_end['time'].tolist()[0])
        # vprint(end)

        # no marker for players that survived
        marker = 'x' if not player_survived else None

        # extend dataset by adding a pre-diff datapoint to each score event
        if(anti_smoothing):
            x = [a for b in zip([xi-1 for xi in x], x) for a in b]
            y = [a for b in zip([0, *y[0:len(y)-1]], y) for a in b]

        # when the player is nuked out, there will be no score delta for that final deac
        # therefore we need to add their end time as a final datapoint, with the last score.
        # this also makes it easy to mark their death on the graph
        x = [*x, end]
        y = [*y, y[-1]]

        ax.plot(x, y,
                color=color,
                linestyle=linestyle,
                marker=marker,
                # mark just the final item
                markevery=[len(x)-1],
                label="%s - %s %s" %
                (player_name, player_team_str, row['position'])
                )

    ax.legend(loc='upper left')
    ax.set(xlim=(0, maxx), ylim=(-1000, maxy))
    ax.grid()

    # plt.margins(x=0, y=0)
    plt.xticks(xticks, [functions.millis_to_msr(xval, 'human')
                        for xval in xticks])
    plt.yticks(yticks)

    if save_file:
        print(data[0])
        game_data = data[0]['start'].to_numpy()[0]
        game_date = game_data[0:8]
        game_number = game_data[8:12]

        new_file_name = '%s_%s.png' % (game_date, game_number)
        print('Saving graph for game %s' % new_file_name)
        plt.savefig(os.path.join(constants.OUTPUTS_DATA_PATH, new_file_name))
        
    if show_plot:
        print('Rendering graph for game %s' % new_file_name)
        plt.show()


# use these two variables to target games with specific dates and game IDs
this_filename = 1942
this_filepath = 20191202

# chart_score(this_filename, "%s%s" % (constants.RAW_DATA_PATH, this_filepath), show_plot=True)
