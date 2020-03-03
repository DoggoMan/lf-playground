# Lfstats API test
import json
import requests
import backoff
import pandas as pd

from common.queries import sample_queries

IS_SCHEMA_CHECK = False
LOG_QUERY = False
LOG_QUERY_RESULT = False
API_URL = "https://lfstats-hasura.herokuapp.com/v1/graphql"

MAX_NAME_LEN = 10
SCREEN_WIDTH = 54


def cprint(text):
    tlen = len(text)
    diff = int((SCREEN_WIDTH - tlen) / 2)
    print(" " * diff + text)


def printHeader(label):
    print("\n" + "-" * SCREEN_WIDTH)
    cprint(label)
    cprint("-" * (len(label)+2))


players = [
    "Rr Uu Ss Tt Yy",
    "Tragedy",
    "J.F.K",
    "Anarki",
    "boomTRAIN",
    "Striker",
    "Glaedr",
    "Screaver",
    "Foxtrot",
    "Scorpion",
    "Troyoda",
    "Basil Brush",
    "Squiza",
    "Shodan",
    "Pupp",
    "Grim Reaper",
    ":^]",
    "Rullet",
    "Quinn",
    # "Nilthing",
    "Fishie",
    "The Scary One",
    "Sgt. Mitchel",
    "Pina Colada",
    "Catclone",
    "El",
    "SmileySniper 🙂",
    "PlasmaPod",
    "Jabba"]

### START FUNCTIONS ###


@backoff.on_exception(backoff.expo,
                      requests.exceptions.RequestException,
                      max_time=30)
def fetchData(query):

    if LOG_QUERY:
        print("Requesting data: ", query, "\n")

    r = requests.post(API_URL, json={'query': query}, timeout=10)

    if r.status_code != 200:
        print(r.status_code)
        print(r.text)
        return None

    json_data = json.loads(r.text)
    if "errors" in json_data.keys():
        print("Found error in query result", r.text)

    if LOG_QUERY_RESULT:
        print(json.dumps(json_data, indent=2, sort_keys=True))

    json_data = json_data["data"]

    if IS_SCHEMA_CHECK:
        print(json.dumps(json_data, indent=2, sort_keys=True))
        exit()

    return json_data


def aggsRowToObject(row):
    name = row["player_name"][:MAX_NAME_LEN]
    aggregate = row["scorecards_aggregate"]["aggregate"]

    return {
        "name": name,
        "avg": aggregate["avg"]["mvp_points"],
        "std":  aggregate["stddev"]["mvp_points"],
        "games": aggregate["count"],
        "max": aggregate["max"]["mvp_points"],
        "min":  aggregate["min"]["mvp_points"],
    }


def renderPlayerScoreAggs(label, data):
    datarows = list(map(aggsRowToObject, data))

    datasorted = []
    for player in players:
        match = [row for row in datarows if row["name"]
                 == player[:MAX_NAME_LEN]]
        if match:
            datasorted.append(match[0])

    df = pd.DataFrame(datasorted, columns=["name", "avg", "std", "games", "max", "min"]
                      )
    df = df.sort_values("avg", ascending=False)

    df = df.round(2)

    printHeader(label)

    print(df)

    return df


def playerRowToObject(row):
    name = row["player_name"][:MAX_NAME_LEN]
    aggregate = row["scorecards"]

    return {
        "name": name,
        "avg": aggregate["avg"]["mvp_points"],
        "std":  aggregate["stddev"]["mvp_points"],
        "games": aggregate["count"],
        "max": aggregate["max"]["mvp_points"],
        "min":  aggregate["min"]["mvp_points"],
    }


def renderPlayerScorecards(label, data):
    datarows = list(map(lambda row: playerRowToObject(row), data))

    datasorted = []
    for player in players:
        match = [row for row in datarows if row["name"]
                 == player[:MAX_NAME_LEN]]
        if match:
            datasorted.append(match[0])

    df = pd.DataFrame(datasorted, columns=["name", "avg", "std", "games", "max", "min"]
                      )
    df = df.sort_values("avg", ascending=False)

    df = df.round(2)

    printHeader(label)
    print(df)

    return df

    """
def dumpAll(**args):
  return (*[json.dumps(item) for item in **args])
  """

### END FUNCTIONS ###


def main():

    if IS_SCHEMA_CHECK:
        query = sample_queries["getTable"]
        query = sample_queries["getTableSimple"]
        fetchData(query)

    future = "2050-01-01"

    ###
    query = sample_queries["getScoreAggs"] % (json.dumps(players), json.dumps(
        "2019-01-01"), json.dumps(future))
    json_data = fetchData(query)
    data = json_data["players"]

    data2019 = renderPlayerScoreAggs("Socials, 2019+", data)

    ###
    query = sample_queries["getScoreAggs"] % (json.dumps(players), json.dumps(
        "2020-01-01"), json.dumps(future))
    json_data = fetchData(query)
    data = json_data["players"]

    data2020 = renderPlayerScoreAggs("Socials, 2020", data)

    ###
    printHeader("Trend 2019 > 2020")
    df = pd.DataFrame(data2019).merge(data2020, how="inner", on="name")

    print(df.columns)
    # print(df[["name","avg_x","avg_y"]])

    df["trend"] = df.apply(lambda row: row["avg_y"] - row["avg_x"], axis=1)

    print(df[["name", "trend", "avg_x", "avg_y"]])
    ###
    center = "-01-01"
    year = 2019
    yearless = str(year - 1) + center
    yearmore = str(year + 1) + center
    printHeader("Trend %s > %s" % (yearless, yearmore))
    dataless = sample_queries["getScoreAggs"] % (json.dumps(
        players), json.dumps("2020-01-01"), json.dumps(future))

    """

  query = getScorecards % (json.dumps(players), json.dumps("2019-01-01"))
  json_data = fetchData(query)

  data = json_data["players"]

  players = []

  for player in data:
    name = player["player_name"]
    games = player["scorecards"]
    # extend game object with the player name
    players.append([dict(game, **{"name": name}) for game in games])
    
  # print(players[0])
    

  df = pd.DataFrame.from_records(players, 
  # columns=["name","avg","std","games","max","min"]
  )

  print(df.iloc[0][:])
  print(df.columns)



  # renderPlayerScorecards("Manual Aggregation, 2019+", data)

  """


if __name__ == "__main__":
    main()
