__author__ = "Danny Regan"
__contributors__ = ["Amanda Menier"]
__created__ = "2025-05-06"
__version__ = "1.0.0"
__last_updated__ = "2025-05-09"
__description__ = "A GUI app that manages the 'league' MySQL database. It provides funtionality for interacting with the database. Users are able to create teams, add players to those teams, input game information and results, and track basic player statistics."


# References:
# https://tkdocs.com/tutorial/
# https://docs.python.org/3/library/tkinter.html#text-widget
# https://www.tutorialspoint.com/python/tk_text.htm
# https://www.youtube.com/watch?v=AK1J8xF4fuk
# https://www.drupal.org/forum/support/module-development-and-code-questions/2007-03-16/d-and-s-in-sql-queries
# https://www.youtube.com/watch?v=B3OCXBL4Hxs -- Generate PDF with Python

from view import app

def main():
    app()

if __name__ == '__main__':
    main()