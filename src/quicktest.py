import api

query = """
query getAliases {
  games(
    limit: 10
  )
  {
    scorecards {
      team_id
      player_id
      mvp_points
      score
    }
  }
}
"""

print("Fetching data for query: ", query)
data = api.fetchData(query)

if data is not None:
    print("Got Data!")
    print(data)
else:
    print("No data returned for query!")


"""
1. get scorecards from match
2. group by team
3. calculate median, mean and std per team


"""
