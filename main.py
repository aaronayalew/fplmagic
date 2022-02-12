from time import sleep
import asyncio
import sys

from fpl import FPL
import aiohttp
import numpy as np
import pandas as pd

def searchPlayer(players, id):
    for player in players:
        if player.id == id: 
            return player

async def getOptimalTeam():
    sys.stdout.write("\rCreating session...") #TODO: Beautify console output 
    session = aiohttp.ClientSession()
    fpl = FPL(session)
    sys.stdout.flush
    sys.stdout.write("\rLoading all players and fixtures...")
    players = await fpl.get_players()
    fixtures = await fpl.get_fixtures_by_gameweek(25)
    scoresDict = {}
    sys.stdout.flush
    sys.stdout.write("\rGoing through the players and fixtures...") 
    for fixture in fixtures :
        sys.stdout.write("\r{0}".format(fixture))
        playersH = filter(lambda player: player.team == fixture.team_h, players)
        playersA = filter(lambda player: player.team == fixture.team_a, players)        
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
            score *= float(player.points_per_game)
            score *= (1 / fixture.team_h_difficulty)
            scoresDict[player.id] = score

    scores = pd.Series(scoresDict)
    bestxindex = scores.nlargest(11)
    bestxi = [searchPlayer(players, id) for id in bestxindex.index.tolist()]
    sys.stdout.flush()
    print("\r")
    print(*bestxi, sep="\n")
    await session.close()

asyncio.run(getOptimalTeam())
