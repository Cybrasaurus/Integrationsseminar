from flask import Blueprint, render_template, request, redirect, url_for, flash

chapter_1 = Blueprint("chapter1", __name__)


# Chapter 1------------------------------------------------------------------------------------------------------------

@chapter_1.route("/chapter_1")
def chapter_1_desc():
    return render_template("chapter_1_desc.html")


@chapter_1.route("/chapter_1_1")
def chapter_1_1():
    return render_template("chapter_1_1.html")


@chapter_1.route("chapter_1_2", methods=["GET", "POST"])
def chapter_1_2_create_db():

    if request.method == 'POST':
        sample_throughput = request.form.get("sample_form")
        print(sample_throughput)

    return render_template("chapter_1_2.html")