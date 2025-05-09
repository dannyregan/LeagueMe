import tabulate

import DAL as dal

def connectToDB(user, password, host, port, database):
    db = dal.DBConnection(user, password, host, port, database)
    connection = db.connect()
    if connection is not False:
        return connection
    else:
        return False

class Views:
    def displayTopScorers(connection):
        data = dal.PlayersDal.top_scorers(connection)
        headers = ['Points', 'Name', 'Team']
        return tabulate.tabulate(data, headers=headers, tablefmt='fancy_grid')
    
    def displayGameResults(connection):
        data = dal.GamesDal.game_results(connection)
        headers = ['Date', 'Home', 'Score', 'Away', 'Score']
        return tabulate.tabulate(data, headers=headers, tablefmt='fancy_grid')
    
    def displayLeagueStandings(connection):
        data = dal.TeamsDal.league_standings(connection)
        headers = ['Team', 'Games Played', 'Wins', 'Losses', 'Ties', 'Win %']
        return tabulate.tabulate(data, headers=headers, tablefmt='fancy_grid')
    
    def displayTeamRoster(connection, teamName):
        tf, data = dal.TeamsDal.team_roster(connection, teamName)
        if tf == True:
            headers = ['Player', 'Number']
            return tabulate.tabulate(data, headers=headers, tablefmt='fancy_grid')
        else:
            return data
        
    def displayTeamSchedule(connection, teamName):
        tf, data = dal.TeamsDal.team_schedule(connection, teamName)
        if tf == True:
            headers = ['Home', 'Away', 'Date', 'Result', 'Season']
            return tabulate.tabulate(data, headers=headers, tablefmt='fancy_grid'), data
        else:
            return data
    
class Teams:
    def addTeam(connection, teamName):
        res = dal.TeamsDal.addTeam(connection, teamName)
        return res
    
class Players:
    def addPlayer(connection, playerName, teamName, jerseyNum):
        res = dal.PlayersDal.addPlayer(connection, playerName, teamName, jerseyNum)
        return res
    
    def deletePlayer(connection, playerName):
        res = dal.PlayersDal.deletePlayer(connection, playerName)
        return res
    
class Games:
    def addGame(connection, homeTeam, awayTeam, date, gameType, completed):
        res = dal.GamesDal.addGame(connection, homeTeam, awayTeam, date, gameType, completed)
        return res
    
    def updateGame(connection, name, date, homeScore, awayScore):
        res = dal.GamesDal.updateGame(connection, name, date, homeScore, awayScore)
        return res
        
class PointsScored:
    def addPointsScored(connection, name, date, points):
        res = dal.PointsScoredDal.addPointsScored(connection, name, date, points)
        return res