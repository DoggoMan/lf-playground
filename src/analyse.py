import os
import json
import numpy as np
import pandas as pd
import matplotlib as plt
from sklearn import datasets, cluster

DATA_PATH = "./src/data/socials_2019plus.json"


def get_specific_card(scorecards, team, position):
    match = [card for card in scorecards if card['team']
             == team and card['position'] == position]
    if(len(match)):
        return match[0]
    else:
        raise Exception(
            f'No {position} on team {team} within scorecards provided: {scorecards}')


def game_to_summary(game_data):
    time = game_data['game_datetime']

    # print(f"Processing game {game_data['type']} : {time}")

    scorecards = game_data['scorecards']

    # print(game_data['game_teams'])
    teams = [team.get('color_normal') for team in game_data['game_teams']]

    # print(teams)

    win_team_colour = game_data['winner']
    loss_team_colour = [team for team in teams
                        if bool(team) and team != win_team_colour][0]

    win_team_scorecards = [
        x for x in scorecards if x['team'] == win_team_colour]
    loss_team_scorecards = [
        x for x in scorecards if x['team'] == loss_team_colour]

    """
    {
      "player_id": 1403,
      "player_name": "Rr Uu Ss Tt Yy",
      "position": "Commander",
      "team": "red",
      "mvp_points": 25.6
    },
    """

    return {
        'GAME_ID': game_data['id'],
        'WIN_TEAM_COLOUR': win_team_colour,
        'LOSS_TEAM_COLOUR': loss_team_colour,
        'WIN_TEAM_SCORE': game_data[f'{win_team_colour}_score'],
        'LOSS_TEAM_SCORE': game_data[f'{loss_team_colour}_score'],
        'ELIMINATION': game_data['red_eliminated'] or game_data['green_eliminated'],
        'TOTAL_PLAYER_COUNT': game_data['scorecards_aggregate']['aggregate']['count'],
        'WIN_PLAYER_COUNT': len(win_team_scorecards),
        'LOSS_PLAYER_COUNT': len(loss_team_scorecards),
        'WIN_COMM_SCORE': get_specific_card(scorecards, win_team_colour, 'Commander')['score'],
        'WIN_HEAVY_SCORE': get_specific_card(scorecards, win_team_colour, 'Heavy Weapons')['score'],
        'WIN_SCOUT_SCORE': get_specific_card(scorecards, win_team_colour, 'Scout')['score'],
        'WIN_AMMO_SCORE': get_specific_card(scorecards, win_team_colour, 'Ammo Carrier')['score'],
        'WIN_MEDIC_SCORE': get_specific_card(scorecards, win_team_colour, 'Medic')['score'],
        'LOSS_COMM_SCORE': get_specific_card(scorecards, loss_team_colour, 'Commander')['score'],
        'LOSS_HEAVY_SCORE': get_specific_card(scorecards, loss_team_colour, 'Heavy Weapons')['score'],
        'LOSS_SCOUT_SCORE': get_specific_card(scorecards, loss_team_colour, 'Scout')['score'],
        'LOSS_AMMO_SCORE': get_specific_card(scorecards, loss_team_colour, 'Ammo Carrier')['score'],
        'LOSS_MEDIC_SCORE': get_specific_card(scorecards, loss_team_colour, 'Medic')['score'],
    }


with open(DATA_PATH, encoding="utf8") as json_file:
    data = json.load(json_file)
data = data['data']['games']

rows = [game_to_summary(game) for game in data]

# print(json.dumps(data[0], indent=2))
print(json.dumps(rows[0], indent=2))

df = pd.DataFrame.from_dict(rows)

if df is not None:
    print(df.columns)
    print(df)
    print((df[df["ELIMINATION"] == 1]).shape)

    # TODO: Feature agglomerate from this dataframe
