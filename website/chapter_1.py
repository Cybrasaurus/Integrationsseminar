import sqlite3

from flask import Blueprint, render_template, request, redirect, url_for, flash
import logging
from .functions_other import read_py_and_return_part as rprp

chapter_1 = Blueprint("chapter1", __name__)
logging.basicConfig(level=logging.INFO)

# Chapter 1------------------------------------------------------------------------------------------------------------

@chapter_1.route("/chapter_1")
def chapter_1_desc():
    return render_template("chapter_1_desc.html")


@chapter_1.route("/chapter_1_1")
def chapter_1_1():
    return render_template("chapter_1_1.html")


@chapter_1.route("chapter_1_2", methods=["GET", "POST"])
def chapter_1_2_create_db():
    # chapter handles the creation of SQL Databases
    import os
    print(os.getcwd())
    if request.method == 'POST':

        # check whether directory in which the databases get created exist, if not create it
        import website.functions_other as f_o
        if f_o.directory_checker_and_creator("/website/sql_handling/databases") is False:
            flash("Could not find proper Path, making directory for database", category="success")

        # check which button is pressed, create DB accordingly
        if request.form["create_db"] == "sqlite_db":
            # create SQLITE Database
            from .sql_handling.SQLITE import sqlite_commands as PYsqlite
            #todo rework return and error handling
            conn_and_cursor = PYsqlite.create_sql_database()
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


    flask_content = rprp("website/chapter_1.py", "chapter_1_2_create_db()")
    sqlite_content = rprp("website/sql_handling/SQLITE/sqlite_commands.py", "create_sql_database()")
    mysql_content = "$$PLACEHOLDER"
    mariadb_content = "$$PLACEHOLDER"

    return render_template("chapter_1_2_sourcecode.html", flask_server_source=flask_content,
                           sqlite_source=sqlite_content, mysql_source=mysql_content, mariadb_source=mariadb_content)


@chapter_1.route("/chapter_1_3", methods=["GET", "POST"])
def chapter_1_3():
    # populate Databases with sample table containing text and integer to test functionality

    if request.method == "POST":

        if request.form["test_db"] == "see_source_code_sqlite":
            return chapter_1_3_sourcecode_sqlite(db_system="chapter_1_3_sqlite_handling")
        elif request.form["test_db"] == "see_source_code_mysql":
            return chapter_1_3_sourcecode_sqlite(db_system="chapter_1_3_mysql_handling")
        elif request.form["test_db"] == "see_source_code_mariadb":
            return chapter_1_3_sourcecode_sqlite(db_system="chapter_1_3_mariadb_handling")

        elif request.form["test_db"] == "test_sqlite":

            # chapter_1_3_sqlite_handling()
            from website.sql_handling.SQLITE.sqlite_commands import sqlite_connection_provider as conn_prov

            sqllite_conn = conn_prov()
            sqlite_cursor = sqllite_conn[1]

            # wierd formatting due to the view in the gray box otherwise breaking, sees indent as spaces and due
            # to the html <pre> tag those get displayed, making centering impossible
            sql_command_create_table = """
Drop TABLE if EXISTS tester;
                
CREATE TABLE tester(
"Name" TEXT NOT NULL,
"Alter" INTEGER NOT NULL)
            """
            sql_command_fill_table = """
INSERT INTO tester VALUES ('Max SQLITEmann', 20)
INSERT INTO tester VALUES ('Max SQLITEmann 2', 22)
            """

            sqlite_cursor.executescript(sql_command_create_table)

            # note that the actual python statement is slightly different from what a normal SQLITE console would take,
            # separated by a comma and a list
            sqlite_cursor.execute("INSERT INTO tester VALUES (?,?)", ["Max SQLITEmann", "20"])
            sqlite_cursor.execute("INSERT INTO tester VALUES (?,?)", ["Max SQLITEmann 2", "22"])

            # select data from Database
            sqlite_cursor.execute("""
                                    SELECT * from tester""")
            rows = sqlite_cursor.fetchall()
            db_return_value = ""
            for row in rows:
                if db_return_value == "":
                    db_return_value = row
                else:
                    db_return_value = f"{db_return_value} \n {row}"

            return render_template("chapter_1_3.html", sql_command_create_table=sql_command_create_table,
                                   sql_command_fill_table=sql_command_fill_table, current_db="SQLITE", db_return_value=
                                   db_return_value)
            # end chapter_1_3_sqlite_handling()
        elif request.form["test_db"] == "test_mysql":
            # chapter_1_3_mysql_handling()

            sql_command_create_table = "$$placeholder" # TODO
            sql_command_fill_table = "$$placeholder"  # TODO
            db_return_value = "$$placeholder"  # TODO

            return render_template("chapter_1_3.html", sql_command_create_table=sql_command_create_table,
                                   sql_command_fill_table=sql_command_fill_table, current_db="MySQL", db_return_value=
                                   db_return_value)
            # end chapter_1_3_mysql_handling()
        elif request.form["test_db"] == "test_mariadb":
            # chapter_1_3_mariadb_handling()

            sql_command_create_table = "$$placeholder"  # TODO
            sql_command_fill_table = "$$placeholder"  # TODO
            db_return_value = "$$placeholder"  # TODO

            return render_template("chapter_1_3.html", sql_command_create_table=sql_command_create_table,
                                   sql_command_fill_table=sql_command_fill_table, current_db="MariaDB", db_return_value=
                                   db_return_value)
            # end chapter_1_3_mariadb_handling()

            # TODO rest of function
    return render_template("chapter_1_3.html")
# end chapter_1_3()


@chapter_1.route("/chapter_1_3_sourcecode_dynamic")
def chapter_1_3_sourcecode_sqlite(db_system):
    flask_server_source = rprp("website/chapter_1.py", f"{db_system}()")
    return render_template("chapter_1_3_sourcecode_dynamic.html", flask_server_source=flask_server_source)


@chapter_1.route("chapter_1_4", methods=["GET", "POST"])
def chapter_1_4():
    current_JSON=""
    if request.method == "POST":
        from website.generate_JSON import Dataset_Generator as gen_J
        if request.form["gen_json"] == "json_basic":
            current_JSON = "$$placeholder"
            current_content_title = "Einfache JSON"
            json_name_gen_parameters = {
                "full_name": True, "suffix": True, "prefix": True,
                "prefix_distribution": 1.0, "suffix_distribution": 1.0
            }
            gen_J(iterations=1, name_bool=True, name_parameters=json_name_gen_parameters, pathing="website/jsons")
            current_JSON = rprp("website/jsons/Dataset0.json", function_name="", json_mode=True)
            return render_template("chapter_1_4.html", current_JSON=current_JSON,
                                   current_content_title=current_content_title)

        elif request.form["gen_json"] == "json_with_dict":
            current_JSON = "$$placeholder"
            current_content_title = "JSON mit Object"
            json_name_gen_parameters = {
                "full_name": True
            }
            gen_J(iterations=1, name_bool=True, name_parameters=json_name_gen_parameters, pathing="website/jsons",
                  address_bool=True)
            current_JSON = rprp("website/jsons/Dataset0.json", function_name="", json_mode=True)
            return render_template("chapter_1_4.html", current_JSON=current_JSON,
                                   current_content_title=current_content_title)

        elif request.form["gen_json"] == "json_with_list":
            current_JSON = "$$placeholder"
            json_name_gen_parameters = {
                "full_name": True
            }
            current_content_title = "JSON mit Array"
            gen_J(iterations=1, name_bool=True, pathing="website/jsons", country_bool=True, country_param=5,
                  name_parameters=json_name_gen_parameters,)
            current_JSON = rprp("website/jsons/Dataset0.json", function_name="", json_mode=True)
            return render_template("chapter_1_4.html", current_JSON=current_JSON,
                                   current_content_title=current_content_title)

        elif request.form["gen_json"] == "json_with_layers":
            current_JSON = "$$placeholder"
            json_name_gen_parameters = {
                "full_name": True
            }
            current_content_title = "JSON mit 4 Ebenen"
            gen_J(iterations=1, pathing="website/jsons", nested_bool=True, nested_parameters={
                "data_per_layer": 3, "amount_layers": 4
            })
            current_JSON = rprp("website/jsons/Dataset0.json", function_name="", json_mode=True)
            return render_template("chapter_1_4.html", current_JSON=current_JSON,
                                   current_content_title=current_content_title)
    return render_template("chapter_1_4.html")

@chapter_1.route("chapter_1_4_sourcecode")
def chapter_1_4_sourcecode():
    json_module_content = rprp("website/generate_JSON.py", "JSON Generator Module")
    return render_template("chapter_1_4_sourcecode.html", json_module_content=json_module_content)


@chapter_1.route("chapter_1_5", methods=["GET", "POST"])
def chapter_1_5():
    # todo add sourcecode for the JSON example
    # todo json sandbox for playing around
    # todo maybe sourcecode for the 8 buttons below
    if request.method == "POST":

        # generate JSON
        from website.generate_JSON import Dataset_Generator as gen_J
        if list(request.form.keys())[0] == "gen_json":
            if request.form["gen_json"] == "json_basic":
                current_JSON = "$$placeholder"
                current_content_title = "Beispiel JSON"
                json_name_gen_parameters = {
                    "full_name": True
                }
                gen_J(iterations=1, name_bool=True, name_parameters=json_name_gen_parameters, pathing="website/jsons")
                current_JSON = rprp("website/jsons/Dataset0.json", function_name="", json_mode=True)
                return render_template("chapter_1_5.html", current_JSON=current_JSON,
                                       current_content_title=current_content_title)

        elif list(request.form.keys())[0] == "sql_datatype":
            # json as sql datatypes, sql standard
            if request.form["sql_datatype"] == "sql_datatypes_sql":
                return render_template("chapter_1_5.html", sql_commands="sql_datatypes_sql")
            # json as sql datatypes, sqlite
            elif request.form["sql_datatype"] == "sql_datatypes_sqlite":
                return render_template("chapter_1_5.html", sql_commands="sql_datatypes_sqlite")
            # json as sql datatypes, mysql
            elif request.form["sql_datatype"] == "sql_datatypes_mysql":
                return render_template("chapter_1_5.html", sql_commands="sql_datatypes_mysql")
            # json as sql datatypes, mariadb
            elif request.form["sql_datatype"] == "sql_datatypes_mariadb":
                return render_template("chapter_1_5.html", sql_commands="sql_datatypes_mariadb")


        elif list(request.form.keys())[0] == "whole_json":
            # json as whole json, sql standard
            if request.form["whole_json"] == "whole_json_sql":
                return render_template("chapter_1_5.html", sql_commands="whole_json_sql")
            # json as whole json, sqlite
            elif request.form["whole_json"] == "whole_json_sqlite":
                return render_template("chapter_1_5.html", sql_commands="whole_json_sqlite")
            # json as whole json, mysql
            elif request.form["whole_json"] == "whole_json_mysql":
                return render_template("chapter_1_5.html", sql_commands="whole_json_mysql")
            # json as whole json, mariadb
            elif request.form["whole_json"] == "whole_json_mariadb":
                return render_template("chapter_1_5.html", sql_commands="whole_json_mariadb")


    return render_template("chapter_1_5.html")
