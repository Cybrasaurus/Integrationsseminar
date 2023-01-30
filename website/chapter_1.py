import copy
import json

from flask import Blueprint, render_template, request, flash
import logging
from .functions_other import read_py_and_return_part as rprp, json_to_list
from .sql_handling.SQLITE.sqlite_commands import json_to_sqlite_format, sqlite_create_table, sqlite_query_whole_table, \
    sqlite_insert_into_table, json_to_sqlite_json

chapter_1 = Blueprint("chapter1", __name__)
logging.basicConfig(level=logging.INFO)


# Chapter 1------------------------------------------------------------------------------------------------------------

@chapter_1.route("/chapter_1")
def chapter_1_desc():
    return render_template("chapter_1_desc.html")


@chapter_1.route("/chapter_1_1", methods=["GET", "POST"])
def chapter_1_1():

    if request.method == 'POST':
        choice = request.form.getlist('question_choices')

        if choice[0] == "choice_2":
            flash("Correct, right choice", category="success")
        else:
            flash("Wrong Choice, try again", category="error")
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
            # todo rework return and error handling
            conn_and_cursor = PYsqlite.create_sql_database()
            logging.info("Created SQLITE Database")
            flash("Success, SQLITE Database created", category="success")

        elif request.form["create_db"] == "mysql_db":
            # create MySQL Database
            logging.error("MYSQL Database not yet implemented")
            flash("Error, MYSQL Database not yet implemented as a OneClick Application", category="error")

        elif request.form["create_db"] == "maria_db":
            # create MariaDB Database
            logging.error("MariaDB Database not yet implemented")
            flash("Error, MariaDB Database not yet implemented as a OneClick Application", category="error")

    return render_template("chapter_1_2.html")


# end chapter_1_2_create_db()


@chapter_1.route("/chapter_1_2_sourcecode")
def chapter_1_2_sourcecode():
    flask_content = rprp("website/chapter_1.py", "chapter_1_2_create_db()")
    sqlite_content = rprp("website/sql_handling/SQLITE/sqlite_commands.py", "create_sql_database()")
    mysql_content = "Not Implemented, as this is not yet possible as a oneclick application, MySQL Drivers need to be installed first"
    mariadb_content = "Not Implemented, as this is not yet possible as a oneclick application, MySQL Drivers need to be installed first"

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
DROP TABLE IF EXISTS tester;
                
CREATE TABLE tester(
"Name" TEXT NOT NULL,
"Alter" INTEGER NOT NULL)
            """

            sql_command_fill_table = """
INSERT INTO tester VALUES ('Sebastian SQLITEmann', 20)
INSERT INTO tester VALUES ('Sebastian SQLITEmann 2', 22)
            """

            sqlite_cursor.executescript(sql_command_create_table)

            # note that the actual python statement is slightly different from what a normal SQLITE console would take,
            # separated by a comma and a list
            sqlite_cursor.execute("INSERT INTO tester VALUES (?,?)", ["Sebastian SQLITEmann", "20"])
            sqlite_cursor.execute("INSERT INTO tester VALUES (?,?)", ["Sebastian SQLITEmann 2", "22"])

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

            # todo maybe rework the return from lists to a dataframe, gotta see how to display that in HTML

            return render_template("chapter_1_3.html", sql_command_create_table=sql_command_create_table,
                                   sql_command_fill_table=sql_command_fill_table, current_db="SQLITE", db_return_value=
                                   db_return_value, sql_command_query="SELECT * from tester")
            # end chapter_1_3_sqlite_handling()
        elif request.form["test_db"] == "test_mysql":
            # chapter_1_3_mysql_handling()

            sql_command_create_table = "$$placeholder"  # TODO
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
    current_JSON = ""
    if request.method == "POST":
        from website.generate_JSON import Dataset_Generator as gen_J
        if request.form["gen_json"] == "json_basic":
            current_JSON = "$$placeholder"
            current_content_title = "Einfache JSON"
            json_name_gen_parameters = {
                "full_name": True, "suffix": True, "prefix": True,
                "prefix_distribution": 1.0, "suffix_distribution": 1.0
            }
            gen_J(iterations=1, name_bool=True, name_parameters=json_name_gen_parameters, json_pathing="website/jsons",
                  json_file_name="chapter_1_4_basic")
            current_JSON = rprp("website/jsons/chapter_1_4_basic.json", function_name="", json_mode=True)
            return render_template("chapter_1_4.html", current_JSON=current_JSON,
                                   current_content_title=current_content_title)

        elif request.form["gen_json"] == "json_with_dict":
            current_JSON = "$$placeholder"
            current_content_title = "JSON mit Object"
            json_name_gen_parameters = {
                "full_name": True
            }
            gen_J(iterations=1, name_bool=True, name_parameters=json_name_gen_parameters, json_pathing="website/jsons",
                  address_bool=True, json_file_name="chapter_1_4_dict")
            current_JSON = rprp("website/jsons/chapter_1_4_dict.json", function_name="", json_mode=True)
            return render_template("chapter_1_4.html", current_JSON=current_JSON,
                                   current_content_title=current_content_title)

        elif request.form["gen_json"] == "json_with_list":
            current_JSON = "$$placeholder"
            json_name_gen_parameters = {
                "full_name": True
            }
            current_content_title = "JSON mit Array"
            gen_J(iterations=1, name_bool=True, json_pathing="website/jsons", country_bool=True, country_param=5,
                  name_parameters=json_name_gen_parameters, json_file_name="chapter_1_4_list")
            current_JSON = rprp("website/jsons/chapter_1_4_list.json", function_name="", json_mode=True)
            return render_template("chapter_1_4.html", current_JSON=current_JSON,
                                   current_content_title=current_content_title)

        elif request.form["gen_json"] == "json_with_layers":
            current_JSON = "$$placeholder"
            json_name_gen_parameters = {
                "full_name": True
            }
            current_content_title = "JSON mit 4 Ebenen"
            gen_J(iterations=1, json_pathing="website/jsons", nested_bool=True, nested_parameters={
                "data_per_layer": 3, "amount_layers": 4
            }, json_file_name="chapter_1_4_4layer")
            current_JSON = rprp("website/jsons/chapter_1_4_4layer.json", function_name="", json_mode=True)
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

        json_name_gen_parameters = {
            "full_name": True
        }
        # generate JSON
        from website.generate_JSON import Dataset_Generator as gen_J
        if list(request.form.keys())[0] == "gen_json":
            if request.form["gen_json"] == "json_basic":
                current_content_title = "Beispiel JSON"

                gen_J(iterations=1, name_bool=True, name_parameters=json_name_gen_parameters,
                      json_pathing="website/jsons", json_file_name="chapter_1_5_json")
                current_JSON = rprp("website/jsons/chapter_1_5_json.json", function_name="", json_mode=True)
                return render_template("chapter_1_5.html", current_JSON=current_JSON,
                                       current_content_title=current_content_title)

            elif request.form["gen_json"] == "json_with_numbers":
                current_content_title = "JSON mit Integer und Float"

                gen_J(iterations=1, name_bool=True, name_parameters=json_name_gen_parameters,
                      json_pathing="website/jsons", json_file_name="chapter_1_5_json", numbers_bool=True)
                current_JSON = rprp("website/jsons/chapter_1_5_json.json", function_name="", json_mode=True)
                return render_template("chapter_1_5.html", current_JSON=current_JSON,
                                       current_content_title=current_content_title)

            elif request.form["gen_json"] == "json_with_everything":
                current_content_title = "große JSON"

                json_name_gen_parameters = {
                    "full_name": True,
                    "prefix": True,
                    "suffix": True
                }

                gen_J(iterations=1, name_bool=True, name_parameters=json_name_gen_parameters,
                      json_pathing="website/jsons", json_file_name="chapter_1_5_json", numbers_bool=True,
                      address_bool=True, country_bool=True, nested_bool=True)
                current_JSON = rprp("website/jsons/chapter_1_5_json.json", function_name="", json_mode=True)
                return render_template("chapter_1_5.html", current_JSON=current_JSON,
                                       current_content_title=current_content_title)

        elif list(request.form.keys())[0] == "sql_datatype":
            current_content_title = "Beispiel JSON"
            #verify JSON has been generated before attempting commands and consequent query
            try:
                current_JSON = rprp("website/jsons/chapter_1_5_json.json", function_name="", json_mode=True)
                current_JSON_as_dict = json.loads(current_JSON)
            except FileNotFoundError:
                gen_J(iterations=1, name_bool=True, name_parameters=json_name_gen_parameters,
                      json_pathing="website/jsons", json_file_name="chapter_1_5_json")
                current_JSON = rprp("website/jsons/chapter_1_5_json.json", function_name="", json_mode=True)
                current_JSON_as_dict = json.loads(current_JSON)
                flash("Warning, JSON did not yet exist, generated a new one")

            # json as sql datatypes, sql standard
            if request.form["sql_datatype"] == "sql_datatypes_sql":
                return render_template("chapter_1_5.html", sql_commands="sql_datatypes_sql")

            # json as sql datatypes, sqlite
            elif request.form["sql_datatype"] == "sql_datatypes_sqlite":

                column_data = json_to_sqlite_format(input_json=current_JSON_as_dict)
                html_display_column_data = json.dumps(column_data, ensure_ascii=False, indent=4)

                html_display_sqlite_commands = sqlite_create_table(tablename="Testing_table", column_data=column_data,
                                                                   return_commands_bool=True)

                json_content_as_list = json_to_list(current_JSON_as_dict)

                html_display_insert_command = sqlite_insert_into_table(table_name="Testing_table",
                                                                       insert_value_list=json_content_as_list,
                                                                       return_command=True)

                query_result = sqlite_query_whole_table(table_name="Testing_table",
                                                        return_list_with_sqlite_command=True)
                html_display_query_result = query_result[0]
                html_display_query_command = query_result[1]
                return render_template("chapter_1_5.html",
                                       current_JSON=current_JSON, current_content_title=current_content_title,
                                       json_data_sql_data_title="JSON Datentypen zu SQL Datentypen",
                                       json_data_sql_data=html_display_column_data,
                                       sql_command_title="SQLITE Create Table Syntax", sql_commands=html_display_sqlite_commands,
                                       sql_insert_title="SQLITE Insert Syntax", sql_insert=html_display_insert_command,
                                       sql_query_title="SQLITE Query Syntax", sql_query=html_display_query_command,
                                       sql_query_result_title="SQLITE Query Result", sql_query_result=html_display_query_result
                                       )

            # json as sql datatypes, mysql
            elif request.form["sql_datatype"] == "sql_datatypes_mysql":
                return render_template("chapter_1_5.html", sql_commands="Not yet implementable as a Oneclick-Application")
            # json as sql datatypes, mariadb
            elif request.form["sql_datatype"] == "sql_datatypes_mariadb":
                return render_template("chapter_1_5.html", sql_commands="Not yet implementable as a Oneclick-Application")


        elif list(request.form.keys())[0] == "whole_json":
            current_content_title = "Beispiel JSON"
            #verify JSON has been generated before attempting commands and consequent query
            try:
                current_JSON = rprp("website/jsons/chapter_1_5_json.json", function_name="", json_mode=True)
                print(f"current_JSON(type:{type(current_JSON)}) = {current_JSON}")
                current_JSON_as_dict = json.loads(current_JSON)
                print(f"current_JSON_as_dict(type:{type(current_JSON_as_dict)}) = {current_JSON_as_dict}")
            except FileNotFoundError:
                gen_J(iterations=1, name_bool=True, name_parameters=json_name_gen_parameters,
                      json_pathing="website/jsons", json_file_name="chapter_1_5_json")
                current_JSON = rprp("website/jsons/chapter_1_5_json.json", function_name="", json_mode=True)
                current_JSON_as_dict = json.loads(current_JSON)
                flash("Warning, JSON did not yet exist, generated a new one")

            # json as whole json, sql standard
            if request.form["whole_json"] == "whole_json_sql":


                return render_template("chapter_1_5.html", sql_commands="whole_json_sql")
            # json as whole json, sqlite
            elif request.form["whole_json"] == "whole_json_sqlite":

                #todo standardise this into one function maybe?

                json_data_sql_data_title = "JSON zu SQL JSON Datentyp"

                sql_command_title = "SQLITE Commands"
                json_data_sql_data = json_to_sqlite_json()
                whole_json_sqlite = current_JSON
                html_display_json_data_sql_data = json.dumps(json_data_sql_data, ensure_ascii=False, indent=4)

                html_display_sqlite_commands = sqlite_create_table(tablename="Testing_table", column_data=json_data_sql_data,
                                                                   return_commands_bool=True)

                json_for_database = json.dumps(current_JSON_as_dict, ensure_ascii=False)

                html_display_insert_command = sqlite_insert_into_table(table_name="Testing_table",
                                                                       insert_value_list=[json_for_database],
                                                                       return_command=True)

                query_result = sqlite_query_whole_table(table_name="Testing_table",
                                                        return_list_with_sqlite_command=True)
                html_display_query_result = query_result[0]
                html_display_query_command = query_result[1]

                return render_template("chapter_1_5.html", current_content_title="Beispiel JSON",
                                       current_JSON=whole_json_sqlite,
                                       json_data_sql_data_title=json_data_sql_data_title,
                                       json_data_sql_data=html_display_json_data_sql_data,
                                       sql_command_title="SQLITE Create Table Syntax",
                                       sql_commands=html_display_sqlite_commands,
                                       sql_insert_title="SQLITE Insert Syntax",
                                       sql_insert=html_display_insert_command,
                                       sql_query_title="SQLITE Query Syntax", sql_query=html_display_query_command,
                                       sql_query_result_title="SQLITE Query Result",
                                       sql_query_result=html_display_query_result

                                       )
            # json as whole json, mysql
            elif request.form["whole_json"] == "whole_json_mysql":
                return render_template("chapter_1_5.html", sql_commands="Not yet implementable as a Oneclick-Application")
            # json as whole json, mariadb
            elif request.form["whole_json"] == "whole_json_mariadb":
                return render_template("chapter_1_5.html", sql_commands="Not yet implementable as a Oneclick-Application")

    return render_template("chapter_1_5.html")

# TODO testing site for comprehension of JSON to sql data types
# TODO kapitel 3.2 in word doc, testumgebgung und Testdaten

