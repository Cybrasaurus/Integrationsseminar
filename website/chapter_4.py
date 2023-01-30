from flask import Blueprint, render_template, request, redirect, url_for, flash

chapter_4 = Blueprint("chapter4", __name__)


# Chapter 4------------------------------------------------------------------------------------------------------------
@chapter_4.route("/chapter_4")
def chapter_4_desc():
    return render_template("chapter_4_desc.html")


@chapter_4.route("/chapter_4_1")
def chapter_4_1():
    return render_template("chapter_4_1.html")