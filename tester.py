from website.sql_handling.SQLITE.sqlite_commands import json_to_sqlite_format, sqlite_create_table

mydict = {
    "Vorname": "Margot",
    "Nachname": "Meyer",
    "Name": "Margot Meyer",

    "nested": ["list 1", "list2"]
}

column_data = json_to_sqlite_format(input_json=mydict, no_sqlite_type_to_str=False)

print(sqlite_create_table(tablename="Testing_table", column_data=column_data, return_commands_bool=True))