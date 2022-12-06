"""
title: Flask Web App for Contacts
author: Joanna Hao
date-created: 2022-12-05
"""
from flask import Flask, render_template, request, redirect
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
    ALERT = ""
    if request.form:
        FIRST_NAME = request.form.get("first_name")  # label name --> variable (name)
        LAST_NAME = request.form.get("last_name")
        EMAIL = request.form.get("email")
        print(FIRST_NAME, LAST_NAME, EMAIL)
        if EMAIL != "" and FIRST_NAME != "":
            if getOneContact(EMAIL) is None:  # if doesn't already exist in the database
                createContact(FIRST_NAME, LAST_NAME, EMAIL)
                ALERT = f"Successfully added {FIRST_NAME}"
            else:
                ALERT = f"A contact with the email {EMAIL} already exists"
        else:
            ALERT = "Please fill in the required fields: First Name and Email"
    QUERY_CONTACTS = getAllContacts()

    # like the index page in CS10
    return render_template("index.html", alert=ALERT, contacts=QUERY_CONTACTS)
    # alert var inside webpage (any word u want), ALERT for var in function


@app.route("/delete/<id>")  # <> to indicate variable that is going to be put into function
def deleteContactPage(id):
    deleteContact(id)
    return redirect('/')  # / represents home page

# --- sqlite --- #
# --- inputs
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


def createContact(f_name, l_name, email):
    global DB_NAME
    CONNECTION = sqlite3.connect(DB_NAME)
    CURSOR = CONNECTION.cursor()
    CURSOR.execute("""
        INSERT INTO
            contacts
        VALUES (
            ?, ?, ?
        )
    ;""", [f_name, l_name, email])
    CONNECTION.commit()
    CONNECTION.close()


# --- processing
def deleteContact(email):
    global DB_NAME
    CONNECTION = sqlite3.connect(DB_NAME)
    CURSOR = CONNECTION.cursor()
    CURSOR.execute("""
        DELETE FROM
            contacts
        WHERE
            email = ?
    ;""", [email])
    CONNECTION.commit()
    CONNECTION.close()


# --- outputs
def getOneContact(email):
    global DB_NAME
    CONNECTION = sqlite3.connect(DB_NAME)
    CURSOR = CONNECTION.cursor()
    contact = CURSOR.execute("""
        SELECT
            *
        FROM
            contacts
        WHERE
            email = ?
    ;""", [email]).fetchone()
    CONNECTION.close()
    return contact


def getAllContacts():
    global DB_NAME
    CONNECTION = sqlite3.connect(DB_NAME)
    CURSOR = CONNECTION.cursor()
    contacts = CURSOR.execute("""
        SELECT
            *
        FROM 
            contacts
        ORDER BY
            first_name
    ;""").fetchall()
    CONNECTION.close()
    return contacts


if __name__ == "__main__":
    if FIRST_RUN:
        createTable()
    app.run(debug=True)

