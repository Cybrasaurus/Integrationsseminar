from flask import Blueprint, render_template, request, redirect, url_for, flash


views = Blueprint("views", __name__)



@views.route("/error")
def error():
    return render_template("404.html")

@views.route("/")
def home():
    return render_template("landing_page.html")



@views.route("/chapters")
def chapters():
    return render_template("chapter_overview.html")














