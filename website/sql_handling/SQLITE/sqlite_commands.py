import sqlite3
import logging


def create_sql_database():
    # create sqlite database
    conn = sqlite3.connect("website/sql_handling/databases/sqlite_database.db")
    # cursor for sending statements to SQL Database
    cursor = conn.cursor()

    return [conn, cursor]
# end create_sql_database()
