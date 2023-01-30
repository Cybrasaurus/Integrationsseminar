
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