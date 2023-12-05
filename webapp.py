#!/usr/bin/env python3

'''
webapp.py

This program acts as the back-end for the NDSmash web application.
It executes queries into the NDSmash database and parses + passes data
to the front-end demo.html page.

'''

from flask import Flask, render_template, url_for, redirect, request, session
from mysql.connector import connect, Error
from graphqlclient import GraphQLClient
import json, time, os
import manualDB as basic
import random

#Flask app initialization
app = Flask(__name__, template_folder='./', static_url_path='/static')
app.secret_key = "penis"
database = connect(host="localhost", user="ogrimald", password="goirish", database="ogrimald")
cursor = database.cursor(buffered=True)
cursor.execute("use ogrimald")

#current tables in db, used to query total # of entries respectively
tables = ['players', 'tournaments', 'sets']

#Queries for all players who use the prefix "ND", or all Notre Dame players.
def ndQuery():
    cursor.execute("select username from players where players.prefix = 'ND'")
    queriedPlayers = [x[0] for x in cursor]
    return queriedPlayers

def usernameQuery():
    cursor.execute("select username from players;")
    players = [x[0] for x in cursor]
    return players

#Counts total # of entries in each table
def getNumbers():
    queriedResult = []
    for table in tables:
        query = "select count(*) from %s" % table
        cursor.execute(query)
        queriedNum = [x[0] for x in cursor]
        for x in queriedNum:
            queriedResult.append(x)
    return queriedResult

#Gets 100 most recent tournaments and returns data as a list of tuples
# (each 6 terms, representing the attributes of a tournament entry)
def getRecentTournaments():
    cursor.execute("select * from tournaments order by date desc limit 100")
    return [x for x in cursor]


#Main function that runs when webapp is started.
@app.route("/demo")
def index():
    #gets ND players, # of entries, and recent tournaments for demo page
    queriedPlayers = ndQuery()
    queriedResult = getNumbers()
    tournaments = getRecentTournaments()

    #sends data to the html template where it is displayed to user
    return render_template("./demo.html", players=queriedPlayers, numPlayers=queriedResult[0], numTournaments = queriedResult[1], numSets = queriedResult[2], tournaments = tournaments)


@app.route("/", methods=["GET", "POST"])
def home():
    namelogov3Ratio = 4.253392812
    namelogov4Ratio = 1.904075714

    players = usernameQuery()

    errorAlert = ""


    if request.method == 'POST':
        searchbar = request.form.get("searchbar")
        playerURL = url_for('players', searchbar=searchbar)
        tournamentURL = url_for('tournaments', searchbar=searchbar)
    else:
        playerURL = url_for('players')
        tournamentURL = url_for('tournaments')


    return render_template("./home.html", languages=players, playerURL=playerURL, tournamentURL=tournamentURL, errorAlert=errorAlert, width=160, height=160)


@app.route("/players", methods=["GET", "POST"])
def players():
    searchbar =  request.form.get("searchbar")

    return render_template("./players.html", searchbar=searchbar)


@app.route("/tournaments", methods=["GET", "POST"])
def tournaments():
    searchbar =  request.form.get("searchbar")

    return render_template("./tournaments.html", searchbar=searchbar)



#runs on localhost, provides a port
app.run(host="0.0.0.0", port=5027)

