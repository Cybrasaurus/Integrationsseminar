from flask import Blueprint, render_template, request, redirect, url_for, flash

chapter_2 = Blueprint("chapter2", __name__)


# Chapter 2------------------------------------------------------------------------------------------------------------
@chapter_2.route("/chapter_2")
def chapter_2_desc():
    return render_template("chapter_2_desc.html")