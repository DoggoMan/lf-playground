"""

Defines some sample queries for easy use

"""

### START QUERIES ###

introspectionFragments = """
fragment FullType on __Type {
  kind
  name
  description
  fields(includeDeprecated: true) {
    name
    description
    args {
      ...InputValue
    }
    type {
      ...TypeRef
    }
    isDeprecated
    deprecationReason
  }
  inputFields {
    ...InputValue
  }
  interfaces {
    ...TypeRef
  }
  enumValues(includeDeprecated: true) {
    name
    description
    isDeprecated
    deprecationReason
  }
  possibleTypes {
    ...TypeRef
  }
}
fragment InputValue on __InputValue {
  name
  description
  type {
    ...TypeRef
  }
  defaultValue
}
fragment TypeRef on __Type {
  kind
  name
  ofType {
    kind
    name
    ofType {
      kind
      name
      ofType {
        kind
        name
        ofType {
          kind
          name
          ofType {
            kind
            name
            ofType {
              kind
              name
              ofType {
                kind
                name
              }
            }
          }
        }
      }
    }
  }
}
"""

sample_queries = {

    "getTables": """
query {
  __schema {
    queryType {
      fields {
        name
        
      }
    }
  }
}
""",

    "getTable": """
query {
  __type (name: "scorecards") {
    ...FullType
  }
}
""" + introspectionFragments,

    "getTableSimple": """
query {
  __type (name: "scorecards" ) {
    name
    fields {
      name
    }
  }
}
""",

    "getTeamDeltas": """
query GetTeamDeltas($id: bigint) {
    team_deltas(
      order_by: { score_time: asc_nulls_last }
      limit: 10
      where: { game_id: { _eq: $id } }
    ) {
      score_time
      delta
      sum
      team_id
      color_desc
    }
  }
""",

    "getScoreAggs": """
query getScoreAggs {
  players (
   where: {
     player_name: { _in: %s }
   }
  ){ 
    player_name
    scorecards_aggregate (
      where: {
        mvp_points: { _gt: 0 }
        center_id: { _eq: 5 }
        event: { is_comp: { _eq: false } }
        game_datetime: { _gt: %s, _lt: %s}
      }
    ) {
      aggregate {
        count
        avg {
          mvp_points
        }
        stddev {
          mvp_points
        }
        min {
          mvp_points
        } 
        max {
          mvp_points
        }
      }
    }
  }
}
""",

    "getScorecards": """
query getScorecards {
  players (
   limit: 100
   where: {
     player_name: { _in: %s }
   }
  ){ 
    player_name
    scorecards (
      where: {
        mvp_points: { _gt: 0 }
        center_id: { _eq: 5 }
        type: { _eq: "social" }
        game_datetime: { _gt: %s}
      }
    ) {
      game_id
      mvp_points
      event {
        id
        is_comp 
      }
      type
    }
  }
}
"""
}
# END QUERIES

endpoints = {
    "__schema": {
        "queryType": {
            "fields": [
                {
                    "name": "centers"
                },
                {
                    "name": "centers_aggregate"
                },
                {
                    "name": "centers_by_pk"
                },
                {
                    "name": "event_teams"
                },
                {
                    "name": "event_teams_aggregate"
                },
                {
                    "name": "event_teams_by_pk"
                },
                {
                    "name": "events"
                },
                {
                    "name": "events_aggregate"
                },
                {
                    "name": "events_by_pk"
                },
                {
                    "name": "game_actions"
                },
                {
                    "name": "game_actions_aggregate"
                },
                {
                    "name": "game_actions_by_pk"
                },
                {
                    "name": "game_deltas"
                },
                {
                    "name": "game_deltas_aggregate"
                },
                {
                    "name": "game_deltas_by_pk"
                },
                {
                    "name": "game_imports"
                },
                {
                    "name": "game_imports_aggregate"
                },
                {
                    "name": "game_imports_by_pk"
                },
                {
                    "name": "game_logs"
                },
                {
                    "name": "game_logs_aggregate"
                },
                {
                    "name": "game_objects"
                },
                {
                    "name": "game_objects_aggregate"
                },
                {
                    "name": "game_objects_by_pk"
                },
                {
                    "name": "game_results"
                },
                {
                    "name": "game_results_aggregate"
                },
                {
                    "name": "game_teams"
                },
                {
                    "name": "game_teams_aggregate"
                },
                {
                    "name": "game_teams_by_pk"
                },
                {
                    "name": "games"
                },
                {
                    "name": "games_aggregate"
                },
                {
                    "name": "games_by_pk"
                },
                {
                    "name": "games_tags"
                },
                {
                    "name": "games_tags_aggregate"
                },
                {
                    "name": "games_tags_by_pk"
                },
                {
                    "name": "hits"
                },
                {
                    "name": "hits_aggregate"
                },
                {
                    "name": "hits_by_pk"
                },
                {
                    "name": "league_games"
                },
                {
                    "name": "league_games_aggregate"
                },
                {
                    "name": "match_penalties"
                },
                {
                    "name": "match_penalties_aggregate"
                },
                {
                    "name": "match_penalties_by_pk"
                },
                {
                    "name": "matches"
                },
                {
                    "name": "matches_aggregate"
                },
                {
                    "name": "matches_by_pk"
                },
                {
                    "name": "penalties"
                },
                {
                    "name": "penalties_aggregate"
                },
                {
                    "name": "penalties_by_pk"
                },
                {
                    "name": "players"
                },
                {
                    "name": "players_aggregate"
                },
                {
                    "name": "players_by_pk"
                },
                {
                    "name": "players_names"
                },
                {
                    "name": "players_names_aggregate"
                },
                {
                    "name": "players_names_by_pk"
                },
                {
                    "name": "rounds"
                },
                {
                    "name": "rounds_aggregate"
                },
                {
                    "name": "rounds_by_pk"
                },
                {
                    "name": "scorecards"
                },
                {
                    "name": "scorecards_aggregate"
                },
                {
                    "name": "scorecards_by_pk"
                },
                {
                    "name": "tags"
                },
                {
                    "name": "tags_aggregate"
                },
                {
                    "name": "tags_by_pk"
                },
                {
                    "name": "team_deltas"
                },
                {
                    "name": "team_deltas_aggregate"
                },
                {
                    "name": "team_penalties"
                },
                {
                    "name": "team_penalties_aggregate"
                },
                {
                    "name": "team_penalties_by_pk"
                }
            ]
        }
    }
}
