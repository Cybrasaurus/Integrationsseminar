from flask import Blueprint, render_template, request, redirect, url_for, flash
import logging

chapter_1 = Blueprint("chapter1", __name__)
logging.basicConfig(level=logging.INFO)

sqlite_connection = None
sqlite_cursor = None


# Chapter 1------------------------------------------------------------------------------------------------------------

@chapter_1.route("/chapter_1")
def chapter_1_desc():
    return render_template("chapter_1_desc.html")


@chapter_1.route("/chapter_1_1")
def chapter_1_1():
    return render_template("chapter_1_1.html")


@chapter_1.route("chapter_1_2", methods=["GET", "POST"])
def chapter_1_2_create_db():
    global sqlite_connection
    global sqlite_cursor
    # chapter handles the creation of SQL Databases

    if request.method == 'POST':
        # check which button is pressed
        if request.form["create_db"] == "sqlite_db":
            # create SQLITE Database
            from .sql_handling.SQLITE import sqlite_commands as PYsqlite
            conn_and_cursor = PYsqlite.create_sql_database()
            sqlite_connection = conn_and_cursor[0]
            sqlite_cursor = conn_and_cursor[1]
            logging.info("Created SQLITE Database")
            flash("Success, SQLITE Database created", category="success")

        elif request.form["create_db"] == "mysql_db":
            # create MySQL Database
            logging.error("MYSQL Database not yet implemented")
            flash("Error, MYSQL Database not yet implemented", category="error")

        elif request.form["create_db"] == "maria_db":
            # create MariaDB Database
            logging.error("MariaDB Database not yet implemented")
            flash("Error, MariaDB Database not yet implemented", category="error")

    return render_template("chapter_1_2.html")
# end chapter_1_2_create_db()


@chapter_1.route("/chapter_1_2_sourcecode")
def chapter_1_2_sourcecode():
    from .functions_other import read_py_and_return_part as rprp

    flask_content = rprp("website/chapter_1.py", "chapter_1_2_create_db()")
    sqlite_content = rprp("website/sql_handling/SQLITE/sqlite_commands.py", "create_sql_database()")
    mysql_content = "$$PLACEHOLDER"
    mariadb_content = "$$PLACEHOLDER"

    return render_template("chapter_1_2_sourcecode.html", flask_server_source=flask_content,
                           sqlite_source=sqlite_content, mysql_source=mysql_content, mariadb_source=mariadb_content)


@chapter_1.route("/chapter_1_3")
def chapter_1_3():
    # populate Databases with sample table containing text and integer to test functionality
    if sqlite_cursor is None:
        flash("Error, no cursor exists yet, type is null")
    else:
        sqlite_cursor.executescript("""
            Drop TABLE if EXISTS tester;
            
            CREATE TABLE tester(
            "Name" TEXT NOT NULL,
            "Alter" INTEGER NOT NULL)
        """)
        sqlite_cursor.execute("INSERT INTO tester VALUES (?,?)", "Max Mustermann", "20")
        # TODO read in the actual sql commands for the web page
    # TODO rest of function
    pass
# end chapter_1_3()


# TODO chapter 1.3 source code page
