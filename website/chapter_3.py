from flask import Blueprint, render_template, request, redirect, url_for, flash

from website.sql_handling.SQLITE.sqlite_commands import sqlite_query_json_whole_table

chapter_3 = Blueprint("chapter3", __name__)


# Chapter 3------------------------------------------------------------------------------------------------------------
@chapter_3.route("/chapter_3")
def chapter_3_desc():

    return render_template("chapter_3_desc.html")

@chapter_3.route("/chapter_3_1", methods=["GET", "POST"])
def chapter_3_1():
    return render_template("chapter_3_1.html")


@chapter_3.route("/chapter_3_2", methods=["GET", "POST"])
def chapter_3_2():
    if request.method == 'POST':
        form = request.form
        first_command = form["select_extract"]
        print(first_command)
        second_command = form["table_name"]
        print(second_command)

        if first_command == "JSON_DATA, $.Hauptdatensatz.Urlaubsdaten.Urlaubsziele[1].Ziel_2" and \
                second_command == "Urlaubsdaten":
            flash("Richtig", category="success")
        else:
            flash("Falsch", category="error")
    return render_template("chapter_3_2.html")


@chapter_3.route("/chapter_3_3", methods=["GET", "POST"])
def chapter_3_3():
    #todo table for comprehension
    return render_template("chapter_3_3.html")
# todo no spaces in created tables and columns, everything with underscore
# TODO maybe remove debug tools in top register


# SELECT JSON_EXTRACT(JSON_DATA, $.Hauptdatensatz.Urlaubsdaten.Urlaubsziele[1].Ziel_2) FROM Urlaubsdaten

@chapter_3.route("/chapter_3_4")
def chapter_3_4():
    return render_template("chapter_3_4.html")

#general info
    info = """
    json_set replace existing, create non-existing
    json_insert only create new, no replace
    json_replace only replace, no creating
#SQLite
    select json_SET, json_insert, json_replace
    delete: select json_remove
#mysql same commands
#mariadb same commands
    """