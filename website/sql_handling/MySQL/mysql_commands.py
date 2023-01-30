"""
The MIT License (MIT)

Copyright (c) <2023> Cybrasaurus

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""
import mysql.connector


def mysql_create_database(database_name:str = "mysql_database"):
    mydb = mysql.connector.connect(
        host="localhost",
        user="secure_user",
        port="32000",
        password="very_secure_password"
    )

    mycursor = mydb.cursor()

    mycursor.execute(f"CREATE DATABASE {database_name}")
    return mycursor


import pymysql.cursors
def mysql_create_table();


    mycursor = mysql_create_database()
    mycursor.execute("CREATE TABLE customers (name VARCHAR(255), address VARCHAR(255))")


def
if __name__ == "__main__":
    mysql_create_database()