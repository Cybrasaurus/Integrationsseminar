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
import sqlite3
import logging


def directory_checker_and_creator(directorypath: str):
    """
    This function checks whether a given directory exists within the project, if not it creates said directory and
    returns false. If it already exists it returns true
    :param directorypath: the path to the directory, relative from the current working directory
    :return: True or False: If Directory exists -> True, else False
    """
    import os
    cwd = os.getcwd()
    goal_wd = directorypath
    full_path = f"{cwd}{goal_wd}"

    if os.path.exists(full_path) is False:
        os.mkdir(full_path)
        return False
    else:
        return True


def create_sql_database():
    # create sqlite database
    conn = sqlite3.connect("website/sql_handling/databases/sqlite_database.db", check_same_thread=False)
    # cursor for sending statements to SQL Database
    cursor = conn.cursor()

    return [conn, cursor]


# end create_sql_database()


def sqlite_connection_provider(path="standard"):
    if path == "standard":
        import os
        cwd = os.getcwd()
        goal_wd = "/website/sql_handling/databases"
        path = f"{cwd}{goal_wd}"

    if directory_checker_and_creator(goal_wd) is False:
        logging.info("Created Directory")

    conn = sqlite3.connect(f"{path}/sqlite_database.db", check_same_thread=False)
    # cursor for sending statements to SQL Database
    cursor = conn.cursor()
    returnvalue = [conn, cursor]
    return returnvalue


def sqlite_query_whole_table(table_name, amount_rows: int = "all", return_pretty_format: bool = True,
                             return_list_with_sqlite_command: bool = False):
    # todo assert for proper values
    pass
    cursor = sqlite_connection_provider()[1]
    sqlite_command = f"SELECT * from {table_name}"
    cursor.execute(sqlite_command)

    if amount_rows == "all":
        rows = cursor.fetchall()
    else:
        rows = cursor.fetchmany(amount_rows)

    if return_pretty_format is True:
        db_return_value = ""
        for row in rows:
            if db_return_value == "":
                db_return_value = row
            else:
                db_return_value = f"{db_return_value} \n {row}"
        if return_list_with_sqlite_command is False:
            return db_return_value
        else:
            return [db_return_value, sqlite_command]
    else:
        if return_list_with_sqlite_command is False:
            return rows
        else:
            return [rows, sqlite_command]

def sqlite_query_json_whole_table(table_name, col_name:str, keys_to_query_in_col:list, amount_rows: int = "all", return_pretty_format: bool = True,
                             return_list_with_sqlite_command: bool = False,
                                  ):

    pass
    cursor = sqlite_connection_provider()[1]
    # todo sqlite return command in pretty

    json_extract_commands = col_name

    for items in keys_to_query_in_col:
        json_extract_commands += f", '{items}'"

    print(json_extract_commands)

    rows = cursor.execute(f"""
        SELECT json_extract({json_extract_commands}) FROM {table_name}
    """).fetchall()

    print(rows)

def sqlite_create_table(tablename: str, column_data: dict, return_commands_bool: bool = False):
    cursor = sqlite_connection_provider()[1]

    drop_command = f"DROP TABLE IF EXISTS {tablename};\n\n"
    create_command = f"CREATE TABLE {tablename}(\n"

    column_commands = ""
    for keys in column_data.keys():
        column_commands += f'"{keys}" {column_data[keys]},\n'

    # remove last comma, causes syntax error
    column_commands = column_commands[:-2]
    final_command = f"""{drop_command}{create_command}{column_commands})"""

    cursor.executescript(final_command)
    if return_commands_bool is True:
        return final_command


def json_to_sqlite_format(input_json, no_sqlite_type_to_str: bool = True):
    # $$docu, this is for splitting the json
    sqlite_format = {}
    for keys in input_json.keys():
        if type(input_json[keys]) == str:
            sqlite_format[str(keys)] = "TEXT NOT NULL"
        elif type(input_json[keys]) == int:
            sqlite_format[str(keys)] = "INTEGER NOT NULL"
        elif type(input_json[keys]) == float:
            sqlite_format[str(keys)] = "REAL NOT NULL"
        else:
            if no_sqlite_type_to_str is True:
                sqlite_format[str(keys)] = "TEXT NOT NULL"
                # todo if this is set to true, then there needs to be a type conversion in the insert into statement
            else:
                sqlite_format[str(keys)] = "BLOB NOT NULL"

    return sqlite_format


def json_to_sqlite_json(column_name:str = "JSON_Data"):

    sqlite_format = {}
    sqlite_format[column_name] = "JSON"

    return sqlite_format


def sqlite_insert_into_table(table_name, insert_value_list, return_command: bool = False):
    insert_value_list_for_statement = ""
    question_mark_list = ""
    for items in insert_value_list:
        if type(items) == str:
            insert_value_list_for_statement += f"'{items}', "
        else:
            insert_value_list_for_statement += f"{items},"
        question_mark_list += "?,"
    insert_value_list_for_statement = insert_value_list_for_statement[:-1]
    question_mark_list = question_mark_list[:-1]
    sqlite_command = f"INSERT INTO {table_name} VALUES(\n{insert_value_list_for_statement})"

    conn_and_cursor = sqlite_connection_provider()
    conn = conn_and_cursor[0]
    cursor = conn_and_cursor[1]
    print(f"insert_value_list = {insert_value_list}")
    cursor.execute(f"INSERT INTO {table_name} VALUES ({question_mark_list})", insert_value_list)
    conn.commit()

    if return_command is True:
        return sqlite_command


if __name__ == "__main__":
    sqlite_insert_into_table(table_name="myTABLE", insert_value_list=["Sebastian SQLITEmann", 20])
