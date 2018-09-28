""" Database.py is a moule to comunicate with a database. """

import sqlite3
import sys
from typing import List

__all__ = ['Database']

class Database:
    """ Database class initializes and manipulates SQLite3 database. """
    def __init__(self):
        self.con = None
        self.cur = None
        self.donelist = 'donelist'
        self.course = 'course'

    def connect_db(self, db_name):
        """ Connect to the database """
        self.con = sqlite3.connect(db_name)
        self.cur = self.con.cursor()

    def close_db(self):
        """ Close the database """
        if self.con:
            self.con.close()

    def create_table(self):
        """
        Create table.

        donelist: Table for registration of date, course name and duration you studied.
        course: Table for validation of course name.
        """
        donelist = ("CREATE TABLE donelist ("
                    "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                    "date TEXT NOT NULL, "
                    "course TEXT NOT NULL, "
                    "duration TEXT NOT NULL)")

        course = ("CREATE TABLE course ("
                  "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                  "name TEXT NOT NULL UNIQUE)")

        self.cur.execute(donelist)
        self.cur.execute(course)
        self.con.commit()

    def show(self, table):
        """  Show table """
        if self.donelist:
            self.cur.execute('SELECT * FROM donelist').fetchall()
        elif self.course:
            self.cur.execute('SELECT * FROM course').fetchall()
        else:
            print("No such table '{}'.".format(table))
            sys.exit()

    def insert_course(self, courses: List[str]):
        """ Insert course name.

        Insert course name into the 'course' table.
        Insertion of the course name which is already registered will be discarded.
        """
        for elem in courses:
            with self.con:
                self.con.execute('INSERT INTO course(name) VALUES (?)', (elem,))
                print("Add '{}' in course.".format(elem))
        return None

    def insert_donelist(self):
        """ Insert donelist.

        Insert donelist into the 'donelist' table.
        The course name must be a registered name in the 'course' table.
        """
