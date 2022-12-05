"""
title: Flask Web App for Contacts
author: Joanna Hao
date-created: 2022-12-05
"""
from flask import Flask, render_template, request
from pathlib import Path
import sqlite3

# --- variables --- #
DB_NAME = "flask.db"
FIRST_RUN = True
if (Path.cwd() / DB_NAME).exists():
    FIRST_RUN = False


# --- FLASK --- #
app = Flask(__name__)  # makes the flask object

@app.route("/", methods=["GET", "POST"])  # default setting = get data (have to actively tell to return data -- security feature) (Get = get info from server, post = post info to server)
def index():
    if request.form:
        FIRST_NAME = request.form.get("first_name")  # label name --> variable (name)
        LAST_NAME = request.form.get("last_name")
        EMAIL = request.form.get("email")
        print(FIRST_NAME, LAST_NAME, EMAIL)
    # like the index page in CS10
    return render_template("index.html")

# --- sqlite --- #
def createTable():
    global DB_NAME
    CONNECTION = sqlite3.connect(DB_NAME)
    CURSOR = CONNECTION.cursor()
    CURSOR.execute("""
        CREATE TABLE
            contacts (
                first_name TEXT NOT NULL,
                last_name TEXT,
                email TEXT PRIMARY KEY
            )
    ;""")
    # no 2 contacts can have the same email --> unique --> primary key
    CONNECTION.commit()
    CONNECTION.close()  # remove bug purposes


if __name__ == "__main__":
    if FIRST_RUN:
        createTable()
    app.run(debug=True)

