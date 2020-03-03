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

data = api.fetchData(query)

print(data)


"""
1. get scorecards from match
2. group by team
3. calculate median, mean and std per team


"""
