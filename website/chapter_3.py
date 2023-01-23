from flask import Blueprint, render_template, request, redirect, url_for, flash

chapter_3 = Blueprint("chapter3", __name__)


# Chapter 3------------------------------------------------------------------------------------------------------------
@chapter_3.route("/chapter_3")
def chapter_3_desc():
    return render_template("chapter_3_desc.html")