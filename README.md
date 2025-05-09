# league.me

This is a Python-based GUI app that manages the 'league' MySQL database. It provides funtionality for interacting with the database. Users are able to create teams, add players to those teams, input game information and results, and track basic player statistics.

## Technologies Used

- Python 3
- MySQL
- mysql-connector-python
- reportlab
- tabulate
- tkinter

## Project Structure

- ReganFinalProject
    - main.py
    - view.py
    - BLL.py
    - DAL.py
    - db_utils.py
    - README.md

## Install Dependencies

On macOS:

```bash
pip3 install mysql-connector-python tabulate reportlab
```

Tkinter should be included with Python. If, you may need to reinstall the latest version of Python.

## Running the Application

 On macOS, start the application by opening the terminal, navigating to the project directory, and running the following command:

```bash
python3 main.py
```

The interface will prompt you to enter the password for the league database to establish a connection. You may need to change the username, host, or port inputs as well.

You can then select options from menu to run the application. Ensure proper formatting of inputs, especially for date and time inputs (yyyy-mm-dd hh:mm:ss).

## Author

This app was created by Danny Regan as the final project for Professor Amanda Menier's Database Principles course at Merrimack College.