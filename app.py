import sqlite3

from flask import Flask, request
import urllib.parse

app = Flask(__name__)
# cur.execute("""CREATE TABLE "main" ("Link" TEXT,"Tags" TEXT);""")


@app.route("/")
def index():
    return "in dev"


@app.route("/api/add")
def addingIntoDB():
    con = sqlite3.connect("data.db")
    cur = con.cursor()

    link = request.args.get("link")
    link = urllib.parse.unquote(link)
    tags = request.args.get("tags")

    tag_list = tags.split(",")
    for tag in tag_list:
        cur.execute(
            f"""INSERT INTO "main"."main"("Link","Tags") VALUES ('{link}','{tag}');"""
        )

    con.commit()
    con.close()
    return ""


@app.route("/api/remove")
def removeLink():
    con = sqlite3.connect("data.db")
    cur = con.cursor()
    link = request.args.get("link")
    cur.execute(f"""DELETE FROM main WHERE Link='{link}'""")
    return ""


@app.route("/api/get/link")
def getByLink():
    con = sqlite3.connect("data.db")
    cur = con.cursor()

    link = request.args.get("link")

    cur.execute(f"""SELECT * from main WHERE link='{link}'""")

    results = cur.fetchall()
    list_to_return = []
    for result in results:
        list_to_return.append(result[1])

    con.close()
    return str(list_to_return)


@app.route("/api/get/tags")
def getByTags():
    con = sqlite3.connect("data.db")
    cur = con.cursor()

    tag = request.args.get("tag")

    cur.execute(f"""SELECT * from main WHERE tags='{tag}'""")

    results = cur.fetchall()
    list_to_return = []
    for result in results:
        list_to_return.append(result[0])
    con.close()
    return str(list_to_return)
