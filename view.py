from tkinter import *

import BLL as bll

def app():
    # GUI set up
    root = Tk()
    connection = bll.connectToDB()
    root.title('league.me')

    # Track if output box has info in it
    currentOutput = {"box": None}

    # Rows/columns expand within the GUI
    for i in range(40):
        root.grid_rowconfigure(i, weight=1)
        root.grid_columnconfigure(i, weight=1)

    def showMainMenu(root, connection):
        root.geometry('1200x700')
        # Clear the GUI
        for widget in root.grid_slaves():
            widget.grid_forget()
        # Add buttons
        leagueStandingsButton = Button(root, text="League Standings", command=lambda: Games.showLeagueStandings(root, connection))
        leagueStandingsButton.grid(row=0, column=0, padx=10, pady=10)

        gameResultsButton = Button(root, text="Game Results", command=lambda: Games.showGameResults(root, connection))
        gameResultsButton.grid(row=0, column=1, padx=10, pady=10)

        topScorersButton = Button(root, text="Top Scorers", command=lambda: Players.showTopScorers(root, connection))
        topScorersButton.grid(row=0, column=2, padx=10, pady=10)

        addTeamButton = Button(root, text="Add Team", command=lambda: Teams.addTeam(root, connection))
        addTeamButton.grid(row=0, column=3, padx=10, pady=10)

        addPlayerButton = Button(root, text="Add Player", command=lambda: Players.addPlayer(root, connection))
        addPlayerButton.grid(row=0, column=4, padx=10, pady=10)

    def displayOutputBox(root, w, h):
        if currentOutput["box"]:
            currentOutput["box"].destroy()
            currentOutput["box"] = None 
        outputBox = Text(root, width=w, height=h)
        outputBox.grid(row=1, column=0, columnspan=6, padx=20, pady=20)
        currentOutput["box"] = outputBox 
        return outputBox

    def showRes(root, connection, res):
        # Clear the GUI
        for widget in root.grid_slaves():
            widget.grid_forget()
        outputBox = displayOutputBox(root, 500, 1)
        outputBox.insert(END, res)
        okay = Button(root, text='Okay', command=lambda: showMainMenu(root, connection))
        okay.grid(row=3, column=0, columnspan=2, pady=10, padx=10, ipadx=100)

    class Players:
        def showTopScorers(root, connection):
            outputBox = displayOutputBox(root, 195, 45)
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
            outputBox = displayOutputBox(root, 35, 1)
            outputBox.delete("1.0", END)
            outputBox.insert(END, res)
            showRes(root, connection, res)

    class Games:
        def showGameResults(root, connection):                
            outputBox = displayOutputBox(root, 195, 45)
            outputText = bll.Views.displayGameResults(connection)
            outputBox.insert(END, outputText)
        
        def showLeagueStandings(root, connection):
            outputBox = displayOutputBox(root, 195, 45)
            outputText = bll.Views.displayLeagueStandings(connection)
            outputBox.insert(END, outputText)

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













    def viewAllTrips(root, connection):
        root.geometry('1200x700')
        outputBox = displayOutputBox(root, 195, 45)
        outputText = printAllTrips(connection)
        outputBox.insert(END, outputText)

    def viewRevenueByVessel(root, connection):
        root.geometry('900x300')
        outputBox = displayOutputBox(root, 45, 10)
        outputText = printTotalRevenueByVessel(connection)
        outputBox.insert(END, outputText)

    def viewPassengers(root, connection):
        root.geometry('900x300')
        outputBox = displayOutputBox(root, 20, 15)
        outputText = printAllPassengers(connection)
        outputBox.insert(END, outputText)

    def submitPassenger(root, connection, name, address, phone):
        res = addPassenger(connection, name, address, phone)
        outputBox = displayOutputBox(root, 35, 1)
        outputBox.delete("1.0", END)
        outputBox.insert(END, res)
        showRes(root, connection, res)

    def submitVessel(root, connection, name, cph):
        res = addVessel(connection, name, cph)
        outputBox = displayOutputBox(root, 35, 1)
        outputBox.delete("1.0", END)
        outputBox.insert(END, res)
        showRes(root, connection, res)

    def submitTrip(root, connection, vesselName, passengerName, dateAndTime, lengthOfTrip, totalPassengers):
        res = addTrip(connection, vesselName, passengerName, dateAndTime, lengthOfTrip, totalPassengers)
        outputBox = displayOutputBox(root, 45, 1)
        outputBox.insert(END, res)
        showRes(root, connection, res)
        
    def addNewPassenger(root, connection):
        root.geometry('350x250')
        for widget in root.grid_slaves():
            widget.grid_forget()
        # Labels
        title = Label(root, text='Add New Passenger')
        title.grid(row=0, columnspan=2)
        nameLabel = Label(root, text='Name')
        nameLabel.grid(row=1, column=0)
        addressLabel = Label(root, text='Address')
        addressLabel.grid(row=2, column=0)
        phoneLabel = Label(root, text='Phone')
        phoneLabel.grid(row=3, column=0)
        # Inputs
        name = Entry(root, width=20)
        name.grid(row=1, column=1, padx=20)
        address = Entry(root, width=20)
        address.grid(row=2, column=1, padx=20)
        phone = Entry(root, width=20)
        phone.grid(row=3, column=1, padx=20)

        submitPassengerButton = Button(root, text='Submit', command=lambda: submitPassenger(root, connection, name.get(), address.get(), phone.get()))
        submitPassengerButton.grid(row=4, column=0, columnspan=2, pady=10, padx=10, ipadx=100)
        
    def addNewVessel(root, connection):
        root.geometry('350x250')
        for widget in root.grid_slaves():
            widget.grid_forget()
        # Labels
        title = Label(root, text='Add New Vessel')
        title.grid(row=0, columnspan=2, padx=5)
        nameLabel = Label(root, text='Vessel Name')
        nameLabel.grid(row=1, column=0, padx=5)
        cphLabel = Label(root, text='Cost Per Hour')
        cphLabel.grid(row=2, column=0, padx=5)
        # Inputs
        name = Entry(root, width=20)
        name.grid(row=1, column=1)
        cph = Entry(root, width=20)
        cph.grid(row=2, column=1)
        # Submit button
        submitVesselButton = Button(root, text='Submit', command=lambda: submitVessel(root, connection, name.get(), cph.get()))
        submitVesselButton.grid(row=3, column=0, columnspan=2, pady=10, padx=10, ipadx=100)

    def addNewTrip(root, connection):
        root.geometry('350x300')
        for widget in root.grid_slaves():
            widget.grid_forget()
        # Labels
        title = Label(root, text='Add New Trip')
        title.grid(row=0, columnspan=2)
        vesselLabel = Label(root, text='Vessel Name')
        vesselLabel.grid(row=1, column=0, padx=5)
        passengerLabel = Label(root, text='Passenger Name')
        passengerLabel.grid(row=2, column=0, padx=5)
        dtLabel = Label(root, text='Date and Time')
        dtLabel.grid(row=3, column=0, padx=5)
        lengthLabel = Label(root, text='Length of Trip')
        lengthLabel.grid(row=4, column=0, padx=5)
        nPassengersLabel = Label(root, text='Total Passengers')
        nPassengersLabel.grid(row=5, column=0, padx=5)
        # Inputs
        vessel = Entry(root, width=20)
        vessel.grid(row=1, column=1)
        passenger = Entry(root, width=20)
        passenger.grid(row=2, column=1)
        dt = Entry(root, width=20)
        dt.grid(row=3, column=1)
        length = Entry(root, width=20)
        length.grid(row=4, column=1)
        nPassengers = Entry(root, width=20)
        nPassengers.grid(row=5, column=1)
        # Submit button
        submitTripButton = Button(root, text='Submit', command=lambda: submitTrip(root, connection, vessel.get(), passenger.get(), dt.get(), length.get(), nPassengers.get()))
        submitTripButton.grid(row=6, column=0, columnspan=2, pady=10, padx=10, ipadx=100)

    def submitSignIn(user, pswd, host, port):
        global connection
        connection = connectToDB(user, pswd, host, port)
        
        if connection:
            showMainMenu(root, connection)
        else:
            root.geometry('500x100')
            # Clear the GUI
            for widget in root.grid_slaves():
                widget.grid_forget()
            outputBox = displayOutputBox(root, 90, 1)
            outputBox.insert(END, 'Unable to sign in. Try again.')

            okay = Button(root, text='Okay', command=lambda: signIn())
            okay.grid(row=2, column=0, columnspan=2, padx=10, ipadx=100)

    def signIn():
        root.geometry('350x200')
        for widget in root.grid_slaves():
            widget.grid_forget()
        # Sign in labels
        title = Label(root, text='Sign In')
        title.grid(row=0, columnspan=2)
        userLabel = Label(root, text='Username')
        userLabel.grid(row=1, column=0, padx=5)
        pswdLabel = Label(root, text='Password')
        pswdLabel.grid(row=2, column=0, padx=5)
        hostLabel = Label(root, text='Hostname')
        hostLabel.grid(row=3, column=0, padx=5)
        portLabel = Label(root, text='Port')
        portLabel.grid(row=4, column=0, padx=5)
        # Sign in inputs
        user = Entry(root, width=20)
        user.grid(row=1, column=1)
        user.insert(0, 'root')
        pswd = Entry(root, width=20)
        pswd.grid(row=2, column=1)
        pswd.insert(0, '')
        host = Entry(root, width=20)
        host.grid(row=3, column=1)
        host.insert(0, '127.0.0.1')
        port = Entry(root, width=20)
        port.grid(row=4, column=1)
        port.insert(0, '3306')

        submitButton = Button(root, text='Sign In', command=lambda: submitSignIn(user.get(), pswd.get(), host.get(), port.get()))
        submitButton.grid(row=5, column=0, columnspan=2, pady=10, padx=10, ipadx=100)

    showMainMenu(root, connection)
    root.mainloop()