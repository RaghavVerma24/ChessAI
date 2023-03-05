import sqlite3

class Db:

    def __init__(self):
        pass

    def get_plays(self):
        conn = sqlite3.connect('games.db')
        print ("Opened database successfully");