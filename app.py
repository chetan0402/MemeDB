import sqlite3

from flask import Flask, request, render_template
import urllib.parse

app = Flask(__name__)
# cur.execute("""CREATE TABLE "main" ("Link" TEXT,"Tags" TEXT);""")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/add")
def addingIntoDB():
    link = request.args.get("link")
    if link == "":
        return ""
    link = urllib.parse.unquote(link)
    tags = request.args.get("tags")
    if tags == "":
        return ""

    tag_list = tags.split(",")

    con = sqlite3.connect("data.db")
    cur = con.cursor()

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
    con.commit()
    con.close()
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

    tags = request.args.get("tags").split(",")
    main_dic = {}
    list_to_return = []
    for tag in tags:
        cur.execute(f"""SELECT * from main WHERE Tags='{tag}'""")

        results = cur.fetchall()

        for result in results:
            try:
                main_dic[result[0]] += 1
            except:
                main_dic[result[0]] = 1

    for key in main_dic.keys():
        if main_dic[key] == len(tags):
            list_to_return.append(key)

    con.close()
    return str(list_to_return)
