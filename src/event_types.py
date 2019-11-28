EVENT_TYPES = [

    ##### MISSION EVENTS #####

    "0100",  # * Mission Start *

    "0101",  # * Mission End *


    ##### ZAP EVENTS #####

    # player shot but missed anything
    "0201",  # NpbXzq  misses

    # player shot but missed target
    "0202",  # fW6rXgn  misses  @178

    # player shot target
    "0203",  # fW6rXgn  zaps  @178

    # player destroyed target with a shot
    "0204",  # fW6rXgn  destroys  @178

    # player zapped player (no-deac)
    "0205",  # fW6rXgn  zaps  #jtdSRJs

    # player zapped player (deac)
    "0206",  # 5rmpgTL  zaps  #txGrFdM


    ##### MISSILE EVENTS #####

    # player missile locking player
    "0300",  # rgzB9p7  locking  #78QYSKb

    # player destroyed target with a missile
    "0303",  # txGrFdM  destroys  @4414

    # player missiled a player
    "0306",  # rgzB9p7  missiles  #txGrFdM


    ##### SPECIALS EVENTS #####

    # player activated rapid fire
    "0400",  # SJ39pC  activates rapid fire

    # player activated a nuke
    "0404",  # txGrFdM  activates nuke

    # player detonated a nuke
    "0405",  # txGrFdM  detonates nuke


    ##### RESUPPLY EVENTS #####

    # player resupplied ammo
    "0500",  # KQxFLK  resupplies  #5rmpgTL

    # player resupplied lives
    "0502",  # NpbXzq  resupplies  #5rmpgTL

    # player boosted ammo
    "0510",  # spFbw  resupplies team

    # player boosted lives
    "0512",  # NpbXzq  resupplies team


    ##### PENALTY EVENTS #####

    # player penalised
    "0600",  # rgzB9p7 is penalised


    ##### MISC EVENTS #####

    # player awarded generator (elimination)
    "0B03",  # fW6rXgn is awarded 	@176

]
