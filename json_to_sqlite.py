import json
import sqlite3
import logging

logging.basicConfig(level=logging.INFO)

logging.debug(sqlite3.sqlite_version)


# TODO automatic programm: https://withdata.com/file-to-db/file-to-table.html
# todo main source: https://www.youtube.com/watch?v=yxuroInnJNs&ab_channel=BryanCafferky


def load_json_names():
    import os

    json_name_list = []

    goal_wd = f"{os.getcwd()}/jsons"
    for file in os.listdir(goal_wd):
        if file.endswith(".json"):
            json_name_list.append(file)
    logging.debug(json_name_list)
    return json_name_list

def load_json(file_name):
    with open(f"jsons/{file_name}.json", encoding="utf-8") as json_data:
        data = json.load(json_data)
    logging.debug(data)
    logging.debug(type(data))
    logging.debug(json.dumps(data, ensure_ascii=False))
    # set ensure_ascii=false as default JSON encoding is 8bit, will return german characters such as äöüß as escaped
    # unicode characters
    return json.dumps(data, ensure_ascii=False)

load_json("Dataset0")

sample_json = {
    "Name": "Bob Bobson",
    "Vorname": "Bob",
    "Nachname": "Bobson",
    "Anrede": "Herr",
    "Titel": None,
    "Adresse": {
        "Straße": "Münchnerstraße",
        "Hausnummer": "27",
        "PLZ": "74760",
        "Stadt": "München"
    }
}

# make permantent database
conn = sqlite3.connect("pythonjsondemo.db")
# cursor for sending statements to SQL Database
cursor = conn.cursor()


def create_table():
    cursor.executescript("""
        DROP TABLE IF EXISTS people;
        
        CREATE TABLE people(
        "UID"	INTEGER NOT NULL,
        "Name"	TEXT NOT NULL,
        "Vorname"	TEXT NOT NULL,
        "Nachname"	TEXT NOT NULL,
        "Anrede"	TEXT,
        "Titel"	TEXT,
        "json_dump" JSON,
        PRIMARY KEY("UID" AUTOINCREMENT))
    """)


def insert_json_as_whole():
    cursor.execute("INSERT INTO people VALUES (?, ?, ?, ?, ?, ?, ?)",
                   [5, "temp_fullname", "tempname", "temp_lastname", "temp_pronoun", "temp_title",
                    #json.dumps(sample_json)
                   load_json("Dataset0")]
                   )
    conn.commit()

#create_table()
insert_json_as_whole()
