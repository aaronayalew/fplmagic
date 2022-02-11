from time import sleep
import asyncio

from fpl import FPL
import aiohttp
import numpy as np
import pandas as pd

async def getOptimalTeam():
    print("Loading fixtures...")
    session = aiohttp.ClientSession()
    fpl = FPL(session)
    print("Loading all players for fixtures")
    fixtures = await fpl.get_fixtures_by_gameweek(25)
    scoresDict = {}
    # print("Obtaining FDR")
    # try :
    #     fdr = await fpl.FDR()
    # except OSError:
    #     print("Timeout retrying ...")
    #     fdr = await fpl.FDR() 
    print("Going through the players...")
    for fixture in fixtures :
        print(fixture)
        teamH = await fpl.get_team(fixture.team_h)
        teamA = await fpl.get_team(fixture.team_a)
        playersH = await teamH.get_players()
        playersA = await teamA.get_players()
        
        for player in playersH:
            score = 0.0
            score += float(player.ict_index)
            score += float(player.goals_scored) * 100
            score += float(player.assists)* 80
            score += float(player.points_per_game)
            score *= (1 / fixture.team_a_difficulty)
            scoresDict[player.id] = score
        for player in playersA:
            score = 0
            score += float(player.ict_index)
            score += float(player.goals_scored) * 100
            score += float(player.assists)* 80
            score += float(player.points_per_game)
            score *= (1 / fixture.team_h_difficulty)
            scoresDict[player.id] = score

    scores = pd.Series(scoresDict)
    print("Getting Best Player")
    idBP = scores.idxmax()
    bestPlayer = await fpl.get_player(idBP)
    print(bestPlayer.web_name)
    await session.close()

asyncio.run(getOptimalTeam())
