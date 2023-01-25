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


def sqlite_query(sqlite_cursor, query_command):
    pass
    sqlite_cursor.execute


if __name__ == "__main__":
    sqlite_connection_provider()
