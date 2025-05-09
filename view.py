import datetime
from tkinter import *
from reportlab.platypus import SimpleDocTemplate, Table
from reportlab.lib.pagesizes import letter

import BLL as bll

def app():
    # GUI set up
    root = Tk()
    connection = bll.connectToDB()
    root.title('league.me')

    # Track if output box has info in it
    currentOutput = {"box": None}

    def showMainMenu(root, connection):
        root.geometry('1200x700')
        # Clear the GUI
        for widget in root.grid_slaves():
            widget.grid_forget()
        # Add buttons
        leagueStandingsButton = Button(root, text="League Standings", command=lambda: Games.showLeagueStandings(root, connection))
        leagueStandingsButton.grid(row=0, column=2, pady=10)

        gameResultsButton = Button(root, text="Game Results", command=lambda: Games.showGameResults(root, connection))
        gameResultsButton.grid(row=0, column=3, pady=10)

        topScorersButton = Button(root, text="Top Scorers", command=lambda: Players.showTopScorers(root, connection))
        topScorersButton.grid(row=0, column=4, pady=10)

        teamRosterButton = Button(root, text="Team Roster", command=lambda: Teams.showTeamRoster(root, connection))
        teamRosterButton.grid(row=0, column=5, pady=10)

        teamScheduleButton = Button(root, text="Team Schedule", command=lambda: Teams.showTeamSchedule(root, connection))
        teamScheduleButton.grid(row=0, column=6, pady=10)

        addTeamButton = Button(root, text="Add Team", command=lambda: Teams.addTeam(root, connection))
        addTeamButton.grid(row=1, column=1, pady=10)

        addPlayerButton = Button(root, text="Add Player", command=lambda: Players.addPlayer(root, connection))
        addPlayerButton.grid(row=2, column=1, pady=10)

        deletePlayerButton = Button(root, text="Delete Player", command=lambda: Players.deletePlayer(root, connection))
        deletePlayerButton.grid(row=3, column=1, pady=10)

        addGameButton = Button(root, text="Add Game", command=lambda: Games.addGame(root, connection))
        addGameButton.grid(row=4, column=1, pady=10)

        updateGameButton = Button(root, text="Update Game Score", command=lambda: Games.updateGame(root, connection))
        updateGameButton.grid(row=5, column=1, pady=10)

        addPointsButton = Button(root, text="Add Player Points", command=lambda: PointsScored.addPointsScored(root, connection))
        addPointsButton.grid(row=6, column=1, pady=10)


    def displayOutputBox(root, w, h):
        showMainMenu(root, connection)
        if currentOutput["box"]:
            currentOutput["box"].destroy()
            currentOutput["box"] = None 
        outputBox = Text(root, width=w, height=h)
        outputBox.grid(row=1, column=2, rowspan=6, columnspan=6, padx=10, pady=10)
        currentOutput["box"] = outputBox 
        return outputBox

    def showRes(root, connection, res):
        showMainMenu(root, connection)
        # Clear the GUI
        for widget in root.grid_slaves():
            widget.grid_forget()
        outputBox = displayOutputBox(root, 100, 1)
        outputBox.insert(END, res)
        okay = Button(root, text='Okay', command=lambda: showMainMenu(root, connection))
        okay.grid(row=4, column=2, columnspan=2, pady=10, padx=10, ipadx=100)

    class Players:
        def showTopScorers(root, connection):
            showMainMenu(root, connection)
            for widget in root.grid_slaves():
                widget.grid_forget()
            outputBox = displayOutputBox(root, 75, 30)
            outputText = bll.Views.displayTopScorers(connection)
            outputBox.insert(END, outputText)

        def addPlayer(root, connection):
            for widget in root.grid_slaves():
                widget.grid_forget()
            # Labels
            title = Label(root, text='Add New Player')
            title.grid(row=0, columnspan=2, padx=5)
            nameLabel = Label(root, text='Name')
            nameLabel.grid(row=1, column=0, padx=5)
            teamLabel = Label(root, text='Team')
            teamLabel.grid(row=2, column=0, padx=5)
            numberLabel = Label(root, text='Number')
            numberLabel.grid(row=3, column=0, padx=5)
            # Inputs
            name = Entry(root, width=20)
            name.grid(row=1, column=1)
            team = Entry(root, width=20)
            team.grid(row=2, column=1)
            number = Entry(root, width=20)
            number.grid(row=3, column=1)
            # Submit button
            submitPlayerButton = Button(root, text='Add Player', command=lambda: Players.submitPlayer(root, connection, name.get(), team.get(), number.get()))
            submitPlayerButton.grid(row=4, column=0, columnspan=2, pady=10, padx=10, ipadx=100)

        def submitPlayer(root, connection, playerName, teamName, number):
            res = bll.Players.addPlayer(connection, playerName, teamName, number)
            outputBox = displayOutputBox(root, 20, 1)
            outputBox.delete("1.0", END)
            outputBox.insert(END, res)
            showRes(root, connection, res)

        def deletePlayer(root, connection):
            for widget in root.grid_slaves():
                widget.grid_forget()
            # Labels
            title = Label(root, text='Delete Player')
            title.grid(row=0, columnspan=2, padx=5)
            nameLabel = Label(root, text='Name')
            nameLabel.grid(row=1, column=0, padx=5)
            # Inputs
            name = Entry(root, width=20)
            name.grid(row=1, column=1)
            # Submit button
            submitDeletePlayerButton = Button(root, text='Delete Player', command=lambda: Players.submitDeletePlayer(root, connection, name.get()))
            submitDeletePlayerButton.grid(row=2, column=0, columnspan=2, pady=10, padx=10, ipadx=100)

        def submitDeletePlayer(root, connection, playerName):
            res = bll.Players.deletePlayer(connection, playerName)
            outputBox = displayOutputBox(root, 35, 1)
            outputBox.delete("1.0", END)
            outputBox.insert(END, res)
            showRes(root, connection, res)

    class Games:
        def showGameResults(root, connection):
            showMainMenu(root, connection)                
            outputBox = displayOutputBox(root, 75,30)
            outputText = bll.Views.displayGameResults(connection)
            outputBox.insert(END, outputText)
        
        def showLeagueStandings(root, connection):
            showMainMenu(root, connection)
            outputBox = displayOutputBox(root, 75, 30)
            outputText = bll.Views.displayLeagueStandings(connection)
            outputBox.insert(END, outputText)

        def addGame(root, connection):
            for widget in root.grid_slaves():
                widget.grid_forget()
            # Labels
            title = Label(root, text='Add New Game')
            title.grid(row=0, columnspan=2, padx=5)
            homeTeamLabel = Label(root, text='Home Team')
            homeTeamLabel.grid(row=1, column=0, padx=5)
            awayTeamLabel = Label(root, text='Away Team')
            awayTeamLabel.grid(row=2, column=0, padx=5)
            dateLabel = Label(root, text='Date YYYY-MM-DD hh:mm:ss')
            dateLabel.grid(row=3, column=0, padx=5)
            seasonLabel = Label(root, text='pre-season, regular-season, or post-season')
            seasonLabel.grid(row=4, column=0, padx=5)
            completedLabel = Label(root, text='Completed')
            completedLabel.grid(row=5, column=0, padx=5)
            # Inputs
            homeTeam = Entry(root, width=20)
            homeTeam.grid(row=1, column=1)
            awayTeam = Entry(root, width=20)
            awayTeam.grid(row=2, column=1)
            date = Entry(root, width=20)
            date.grid(row=3, column=1)
            season = Entry(root, width=20)
            season.grid(row=4, column=1)
            # Checkbox
            completed_var = BooleanVar()
            completed = Checkbutton(root, variable=completed_var)
            completed.grid(row=5, column=1)

            # Submit button
            submitGameButton = Button(root, text='Add Game', command=lambda: Games.submitGame(root, connection, homeTeam.get(), awayTeam.get(), date.get(), season.get(), completed_var.get()))
            submitGameButton.grid(row=6, column=1, columnspan=2, pady=10, padx=10, ipadx=100)

        def submitGame(root, connection, homeTeam, awayTeam, date, gameType, completed):
            res = bll.Games.addGame(connection, homeTeam, awayTeam, date, gameType, completed)
            outputBox = displayOutputBox(root, 35, 1)
            outputBox.delete("1.0", END)
            outputBox.insert(END, res)
            showRes(root, connection, res)

        def updateGame(root, connection):
            for widget in root.grid_slaves():
                widget.grid_forget()
            # Labels
            title = Label(root, text='Update Game')
            title.grid(row=0, columnspan=2, padx=5)
            teamLabel = Label(root, text='Either Team Name')
            teamLabel.grid(row=1, column=0, padx=5)
            dateLabel = Label(root, text='Date YYYY-MM-DD hh:mm:ss')
            dateLabel.grid(row=2, column=0, padx=5)
            homeScoreLabel = Label(root, text='Home Score')
            homeScoreLabel.grid(row=3, column=0, padx=5)
            awayScoreLabel = Label(root, text='Away Score')
            awayScoreLabel.grid(row=4, column=0, padx=5)
            # Inputs
            team = Entry(root, width=20)
            team.grid(row=1, column=1)
            date = Entry(root, width=20)
            date.grid(row=2, column=1)
            homeScore = Entry(root, width=20)
            homeScore.grid(row=3, column=1)
            awayScore = Entry(root, width=20)
            awayScore.grid(row=4, column=1)
            # Submit button
            submitUpdateGameButton = Button(root, text='Update Game', command=lambda: Games.submitUpdateGame(root, connection, team.get(), date.get(), homeScore.get(), awayScore.get()))
            submitUpdateGameButton.grid(row=5, column=1, columnspan=2, pady=10, padx=10, ipadx=100)

        def submitUpdateGame(root, connection, name, date, homeScore, awayScore):
            res = bll.Games.updateGame(connection, name, date, homeScore, awayScore)
            outputBox = displayOutputBox(root, 35, 1)
            outputBox.delete("1.0", END)
            outputBox.insert(END, res)
            showRes(root, connection, res)

    class Teams:
        def addTeam(root, connection):
            for widget in root.grid_slaves():
                widget.grid_forget()
            # Labels
            title = Label(root, text='Add New Team')
            title.grid(row=0, columnspan=2, padx=5)
            nameLabel = Label(root, text='Team Name')
            nameLabel.grid(row=1, column=0, padx=5)
            # Inputs
            name = Entry(root, width=20)
            name.grid(row=1, column=1)
            # Submit button
            submitTeamButton = Button(root, text='Add Team', command=lambda: Teams.submitTeam(root, connection, name.get()))
            submitTeamButton.grid(row=3, column=0, columnspan=2, pady=10, padx=10, ipadx=100)

        def submitTeam(root, connection, teamName):
            res = bll.Teams.addTeam(connection, teamName)
            outputBox = displayOutputBox(root, 35, 1)
            outputBox.delete("1.0", END)
            outputBox.insert(END, res)
            showRes(root, connection, res)

        def showTeamSchedule(root, connection):
            for widget in root.grid_slaves():
                widget.grid_forget()
            # Labels
            title = Label(root, text='Enter Team Name')
            title.grid(row=0, columnspan=2, padx=5)
            nameLabel = Label(root, text='Team Name')
            nameLabel.grid(row=1, column=0, padx=5)
            # Inputs
            name = Entry(root, width=20)
            name.grid(row=1, column=1)
            # Submit button
            submitShowTeamScheduleButton = Button(root, text='View Schedule', command=lambda: Teams.submitShowTeamSchedule(root, connection, name.get()))
            submitShowTeamScheduleButton.grid(row=2, column=0, columnspan=2, pady=10, padx=10, ipadx=100)

        def showTeamRoster(root, connection):
            showMainMenu(root, connection)
            for widget in root.grid_slaves():
                widget.grid_forget()
            # Labels
            title = Label(root, text='Enter Team Name')
            title.grid(row=0, columnspan=2, padx=5)
            nameLabel = Label(root, text='Team Name')
            nameLabel.grid(row=1, column=0, padx=5)
            # Inputs
            name = Entry(root, width=20)
            name.grid(row=1, column=1)
            # Submit button
            submitShowTeamRosterButton = Button(root, text='View Roster', command=lambda: Players.submitShowTeamRoster(root, connection, name.get()))
            submitShowTeamRosterButton.grid(row=2, column=0, columnspan=2, pady=10, padx=10, ipadx=100)

        def submitShowTeamRoster(root, connection, teamName):
            showMainMenu(root, connection)
            outputBox = displayOutputBox(root, 75, 35)
            outputText = bll.Views.displayTeamRoster(connection, teamName)
            outputBox.delete("1.0", END)
            outputBox.insert(END, outputText)

        # My advanced feature lets you download the schedule as a pdf
        # https://www.youtube.com/watch?v=B3OCXBL4Hxs
        def getPdf(data, teamName):
            filename = f"{teamName}-schedule.pdf" # Creates filename
            pdf = SimpleDocTemplate( # Creates a blank pdf file
                filename,
                pagesize=letter
            )
            # Removes 'datetime.datetime' from the data
            formatted_data = [
                tuple(item.strftime("%Y-%m-%d %H:%M") if isinstance(item, datetime.datetime) else item for item in row)
                for row in data
            ]
            headers = ['Home', 'Away', 'Date', 'Result', 'Type']
            # Appends headers to the data
            formatted_and_headers = [headers] + formatted_data
            # Creates a table with the data
            table = Table(formatted_and_headers)
            elems = []
            elems.append(table) # Insert the table into an array
            pdf.build(elems) # Fill the pdf with the table
            # Provide user with a message
            title = Label(root, text='PDF added to the directory in which this app is saved.')
            title.grid(row=8, column=2, columnspan=4)

        def submitShowTeamSchedule(root, connection, teamName):
            showMainMenu(root, connection)
            outputBox = displayOutputBox(root, 75, 35)
            outputText, data = bll.Views.displayTeamSchedule(connection, teamName)
            getPdfButton = Button(root, text='Get PDF Schedule', command=lambda: Teams.getPdf(data, teamName))
            getPdfButton.grid(row=7, column=2, columnspan=2, pady=10, padx=10)
            outputBox.delete("1.0", END)
            outputBox.insert(END, outputText)

    class PointsScored:
        def addPointsScored(root, connection):
            for widget in root.grid_slaves():
                widget.grid_forget()
            # Labels
            title = Label(root, text='Input Points Scored')
            title.grid(row=0, columnspan=2, padx=5)
            title = Label(root, text='NOTE: THIS WILL AFFECT THE GAME SCORE')
            title.grid(row=1, columnspan=2, padx=5)
            nameLabel = Label(root, text='Player Name')
            nameLabel.grid(row=2, column=0, padx=5)
            dateLabel = Label(root, text='Date YYYY-MM-DD hh:mm:ss')
            dateLabel.grid(row=3, column=0, padx=5)
            pointsLabel = Label(root, text='Points')
            pointsLabel.grid(row=4, column=0, padx=5)
            # Inputs
            name = Entry(root, width=20)
            name.grid(row=2, column=1)
            date = Entry(root, width=20)
            date.grid(row=3, column=1)
            points = Entry(root, width=20)
            points.grid(row=4, column=1)
            # Submit button
            submitPointsButton = Button(root, text='Add Points', command=lambda: PointsScored.submitPointsScored(root, connection, name.get(), date.get(), points.get()))
            submitPointsButton.grid(row=5, column=0, columnspan=2, pady=10, padx=10, ipadx=100)

        def submitPointsScored(root, connection, name, date, points):
            res = bll.PointsScored.addPointsScored(connection, name, date, points)
            outputBox = displayOutputBox(root, 35, 1)
            outputBox.delete("1.0", END)
            outputBox.insert(END, res)
            showRes(root, connection, res)

    # def submitSignIn(user, pswd, host, port):
    #     global connection
    #     connection = connectToDB(user, pswd, host, port)
        
    #     if connection:
    #         showMainMenu(root, connection)
    #     else:
    #         root.geometry('500x100')
    #         # Clear the GUI
    #         for widget in root.grid_slaves():
    #             widget.grid_forget()
    #         outputBox = displayOutputBox(root, 90, 1)
    #         outputBox.insert(END, 'Unable to sign in. Try again.')

    #         okay = Button(root, text='Okay', command=lambda: signIn())
    #         okay.grid(row=2, column=0, columnspan=2, padx=10, ipadx=100)

    # def signIn():
    #     root.geometry('350x200')
    #     for widget in root.grid_slaves():
    #         widget.grid_forget()
    #     # Sign in labels
    #     title = Label(root, text='Sign In')
    #     title.grid(row=0, columnspan=2)
    #     userLabel = Label(root, text='Username')
    #     userLabel.grid(row=1, column=0, padx=5)
    #     pswdLabel = Label(root, text='Password')
    #     pswdLabel.grid(row=2, column=0, padx=5)
    #     hostLabel = Label(root, text='Hostname')
    #     hostLabel.grid(row=3, column=0, padx=5)
    #     portLabel = Label(root, text='Port')
    #     portLabel.grid(row=4, column=0, padx=5)
    #     # Sign in inputs
    #     user = Entry(root, width=20)
    #     user.grid(row=1, column=1)
    #     user.insert(0, 'root')
    #     pswd = Entry(root, width=20)
    #     pswd.grid(row=2, column=1)
    #     pswd.insert(0, '')
    #     host = Entry(root, width=20)
    #     host.grid(row=3, column=1)
    #     host.insert(0, '127.0.0.1')
    #     port = Entry(root, width=20)
    #     port.grid(row=4, column=1)
    #     port.insert(0, '3306')

    #     submitButton = Button(root, text='Sign In', command=lambda: submitSignIn(user.get(), pswd.get(), host.get(), port.get()))
    #     submitButton.grid(row=5, column=0, columnspan=2, pady=10, padx=10, ipadx=100)

    showMainMenu(root, connection)
    root.mainloop()