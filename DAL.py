import mysql.connector

import db_utils

class DBConnection:
#     def __init__(self, user, password, host, port):
    def __init__(self):
    # self.password = password
    # self.user = user
    # self.host = host
    # self.port = port
        self.config = {
    #   'user': self.user,
    #   'password': self.password,
    #   'host': self.host,
    #   'port': self.port,
            'user': 'root',
            'password': 'legends',
            'host': '127.0.0.1',
            'port': '3306',
            'database': 'league'
        }
        self.connection = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(**self.config)
            return self.connection
        except:
            return self.connection
  
    def cursor(self):
        if self.connection:
            return self.connection.cursor()
        else:
            return "Not connected to a database."
  
    def close(self):
        if self.connection:
            self.connection.close()
            self.connection = None

class TeamsDal:
    def league_standings(connection):
        connection = db_utils.ensure_connection(connection)
        cursor = connection.cursor()
        query = "CALL showLeagueStandings();"
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result
    
    def team_roster(connection, teamName):
        connection = db_utils.ensure_connection(connection)
        cursor = connection.cursor()
        try:
            cursor.callproc("getTeamRoster", (teamName,))
            for result in cursor.stored_results():
                fetched = result.fetchall()
                if not fetched:
                    return False, 'Roster not found. Try again.'
                return True, fetched
        except Exception as e:
            print(e)
            return False, 'Unable to find roster.'
        finally:
            cursor.close()

    def team_schedule(connection, teamName):
        connection = db_utils.ensure_connection(connection)
        cursor = connection.cursor()
        try:
            cursor.callproc("getTeamSchedule", (teamName,))
            for result in cursor.stored_results():
                fetched = result.fetchall()
                if not fetched:
                    return False, 'Schedule not found. Try again.'
                return True, fetched
        except Exception as e:
            print(e)
            return False, 'Unable to find schedule.'
        finally:
            cursor.close()
    
    def addTeam(connection, teamName):
        connection = db_utils.ensure_connection(connection)
        cursor = connection.cursor()
        try:
            cursor.callproc("addTeam", (teamName,))
            connection.commit()
            return f'{teamName} are in the league.'
        except Exception as e:
            print(e)
            return 'Team was unable to be added.'
        finally:
            cursor.close()
  
class PlayersDal:
    def top_scorers(connection):
        connection = db_utils.ensure_connection(connection)
        cursor = connection.cursor()
        query = "SELECT * FROM top_scorers;"
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result
    
    def addPlayer(connection, playerName, teamName, jerseyNum):
        connection = db_utils.ensure_connection(connection)
        cursor = connection.cursor()
        try:
            cursor.callproc("addPlayer", (playerName, teamName, jerseyNum,))
            connection.commit()
            for result in cursor.stored_results():
                res = result.fetchone()
                break
            if res[0] == -1:
                return 'Player unable to be added. Another player with that name already exists, or the team does not exist.'
            connection.commit()
            return f'{playerName} has been added.'
        except mysql.connector.Error as e:
            print(e)
            if e.errno == 1172:
                return 'Player was not added. A player with that name already exists.'
            return 'Player was unable to be added.'
        finally:
            cursor.close()

    def deletePlayer(connection, playerName):
        connection = db_utils.ensure_connection(connection)
        cursor = connection.cursor()
        try:
            cursor.callproc("deletePlayer", (playerName,))
            connection.commit()
            return f'{playerName} has been deleted.'
        except mysql.connector.Error as e:
            print(e)
            return 'Player was unable to be added.'
        finally:
            cursor.close()
  
class GamesDal:
    def game_results(connection):
        connection = db_utils.ensure_connection(connection)
        cursor = connection.cursor()
        query = "SELECT * FROM game_results;"
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result
    
    def addGame(connection, homeTeam, awayTeam, date, gameType, completed):
        connection = db_utils.ensure_connection(connection)
        cursor = connection.cursor()
        try:
            cursor.callproc("addgame", (homeTeam, awayTeam, date, gameType, completed,))
            for result in cursor.stored_results():
                res = result.fetchone()
                break
            if res[0] == -1:
                return 'Team not found. Add the team first or try again.'
            connection.commit()
            return 'Game has been added.'
        except Exception as e:
            print(e)
            return 'Game was unable to be added. Check your inputs and try again.'
        finally:
            cursor.close()

    def updateGame(connection, name, date, homeScore, awayScore):
        connection = db_utils.ensure_connection(connection)
        cursor = connection.cursor()
        try:
            cursor.callproc("updateGame", (name, date, homeScore, awayScore,))
            res = None
            for result in cursor.stored_results():
                res = result.fetchone()
                break
            if res and res[0] == -1:
                return 'Game not found. Try again.'
            cursor.callproc("updateGameStatus", (name, date,))
            connection.commit()
            return 'Game has been updated.'
        except Exception as e:
            print(e)
            return 'Game was unable to be updated. Check your inputs and try again.'
        finally:
            cursor.close()
  
class PointsScoredDal:
    def addPointsScored(connection, name, date, points):
        connection = db_utils.ensure_connection(connection)
        cursor = connection.cursor()
        try:
            cursor.callproc("addPointsScored", (name, date, points,))
            res = None
            for result in cursor.stored_results():
                res = result.fetchone()
                break
            if res and res[0] == -1:
                return 'Game or player not found. Try again.'
            connection.commit()
            return f'Point(s) added.'
        except Exception as e:
            print(e)
            return 'Point(s) unable to be added.'
        finally:
            cursor.close()