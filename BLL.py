import tabulate

import DAL as dal

def connectToDB():
    db = dal.DBConnection()
    connection = db.connect()
    if connection:
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
        headers = ['Team', 'Games Played', 'Wins', 'Losses', 'Win %']
        return tabulate.tabulate(data, headers=headers, tablefmt='fancy_grid')
    
class Teams:
    def addTeam(connection, teamName):
        res = dal.TeamsDal.addTeam(connection, teamName)
        return res