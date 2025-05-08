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

  
    # def getVesselID(connection, vesselName):
    #     cursor = connection.cursor()
    #     query = f"SELECT getVesselID('{vesselName}');"
    #     cursor.execute(query)
    #     result = cursor.fetchone()
    #     cursor.close()
    #     if result and result[0] != -1:
    #         return result[0]
    #     else: 
    #         return "Vessel not found."
    
    # def addVessel(connection, name, cph):
    #     cursor = connection.cursor()
    #     try:
    #         cursor.execute("SELECT getVesselID(%s)", (name,))
    #         result = cursor.fetchone()

    #         if result and result[0] == -1:
    #             args = (name, cph)
    #             cursor.callproc("addVessel", args)
    #             connection.commit()
    #             return 'Vessel added successfully.'
    #         else:
    #             return 'Vessel already exists.'
    #     except:
    #         return 'Vessel was unable to be added.'
    #     finally:
    #         cursor.close()
  
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
            return f'{playerName} is in the league.'
        except Exception as e:
            print(e)
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
        except Exception as e:
            print(e)
            return 'Player was unable to be deleted.'
        finally:
            cursor.close()
    
    # def addTrip(connection, vesselName, passengerName, dateAndTime, lengthOfTrip, totalPassengers):
    #     cursor = connection.cursor()
    #     try:
    #         # Set start and end time
    #         startTime = dateAndTime
    #         cursor.execute("SELECT DATE_ADD(%s, INTERVAL %s HOUR)", (dateAndTime, lengthOfTrip))
    #         endTime = cursor.fetchone()[0]

    #         # Get passenger and vessel IDs
    #         cursor.execute("SELECT getPassengerID(%s)", (passengerName,))
    #         passenger_id = cursor.fetchone()[0]

    #         cursor.execute("SELECT getVesselID(%s)", (vesselName,))
    #         vessel_id = cursor.fetchone()[0]

    #         # See if the ends of the trips overlap for the passenger
    #         cursor.execute("""
    #             SELECT COUNT(*) FROM Trips
    #             WHERE passengerID = %s
    #                 AND (%s < DATE_ADD(dateAndTime, INTERVAL lengthOfTrip HOUR))
    #                 AND (dateAndTime < %s)
    #         """, (passenger_id, startTime, endTime))
    #         passenger_overlap = cursor.fetchone()[0]

    #         # See if the ends of the trips overlap for the vessel
    #         cursor.execute("""
    #             SELECT COUNT(*) FROM Trips
    #             WHERE vesselID = %s
    #                 AND (%s < DATE_ADD(dateAndTime, INTERVAL lengthOfTrip HOUR))
    #                 AND (dateAndTime < %s)
    #         """, (vessel_id, startTime, endTime))
    #         vessel_overlap = cursor.fetchone()[0]

    #         if passenger_overlap > 0 or vessel_overlap > 0:
    #             return "Unable to add trip. That passenger or vessel is already booked during this time."

    #         args = (vesselName, passengerName, dateAndTime, lengthOfTrip, totalPassengers)
    #         cursor.callproc("addTrip", args)

    #         for result in cursor.stored_results():
    #             data = result.fetchall()
    #             if data:
    #                 res = data[0][0]
    #                 if res == -3:
    #                     return "Vessel and passenger not found. Add them then try again."
    #                 if res == -2:
    #                     return "Passenger not found. Add them then try again."
    #                 if res == -1:
    #                     return "Vessel not found. Add it then try again."

    #         connection.commit()
    #         return "Trip added successfully."

    #     except:
    #         return "Unable to add trip. Check your inputs and try again."
    #     finally:
    #         cursor.close()
  
    # def allTrips(connection):
    #     cursor = connection.cursor()
    #     query = "SELECT * FROM AllTrips;"
    #     cursor.execute(query)
    #     result = cursor.fetchall()
    #     cursor.close()
    #     return result
  
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
    
    # def addPassenger(connection, passengerName, address, phone):
    #     cursor = connection.cursor()
    #     try:
    #         cursor.execute("SELECT getPassengerID(%s)", (passengerName,))
    #         result = cursor.fetchone()

    #         if result and result[0] == -1:
    #             args = (passengerName, address, phone)
    #             cursor.callproc("addPassenger", args)
    #             connection.commit()
    #             return 'Passenger added successfully.'
    #         else:
    #             return 'Passenger already exists.'
    #     except:
    #         return 'Passenger was unable to be added.'
    #     finally:
    #         cursor.close()
  
    # def getPassengerID(connection, passengerName):
    #     cursor = connection.cursor()
    #     query = f"SELECT getPassengerID('{passengerName}');"
    #     cursor.execute(query)
    #     result = cursor.fetchone()
    #     cursor.close()
    #     if result and result[0] != -1:
    #         return result[0]
    #     else:
    #         return False
    
    # def allPassengers(connection):
    #     cursor = connection.cursor()
    #     query = "SELECT name FROM passengers;"
    #     cursor.execute(query)
    #     result = cursor.fetchall()
    #     cursor.close()
    #     return result
  
class PointsScoredDal:
    def addPointsScored(connection, name, date, points):
        connection = db_utils.ensure_connection(connection)
        cursor = connection.cursor()
        try:
            cursor.callproc("addPointsScored", (name, date, points,))
            connection.commit()
            return f'Point(s) added.'
        except Exception as e:
            print(e)
            return 'Point(s) unable to be added.'
        finally:
            cursor.close()


    # def addPassenger(connection, passengerName, address, phone):
    #     cursor = connection.cursor()
    #     try:
    #         cursor.execute("SELECT getPassengerID(%s)", (passengerName,))
    #         result = cursor.fetchone()

    #         if result and result[0] == -1:
    #             args = (passengerName, address, phone)
    #             cursor.callproc("addPassenger", args)
    #             connection.commit()
    #             return 'Passenger added successfully.'
    #         else:
    #             return 'Passenger already exists.'
    #     except:
    #         return 'Passenger was unable to be added.'
    #     finally:
    #         cursor.close()
  
    # def getPassengerID(connection, passengerName):
    #     cursor = connection.cursor()
    #     query = f"SELECT getPassengerID('{passengerName}');"
    #     cursor.execute(query)
    #     result = cursor.fetchone()
    #     cursor.close()
    #     if result and result[0] != -1:
    #         return result[0]
    #     else:
    #         return False
    
    # def allPassengers(connection):
    #     cursor = connection.cursor()
    #     query = "SELECT name FROM passengers;"
    #     cursor.execute(query)
    #     result = cursor.fetchall()
    #     cursor.close()
    #     return result