#!/usr/bin/env python3

'''
webapp.py

This program acts as the back-end for the NDSmash web application.
It executes queries into the NDSmash database and parses + passes data
to the front-end demo.html page.

'''

from flask import Flask, render_template
from mysql.connector import connect, Error
from graphqlclient import GraphQLClient
import json, time, os
import manualDB as basic
import random

#Flask app initialization
app = Flask(__name__, template_folder='./', static_url_path='/static')
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
@app.route("/")
def index():
    #gets ND players, # of entries, and recent tournaments for demo page
    queriedPlayers = ndQuery()
    queriedResult = getNumbers()
    tournaments = getRecentTournaments()

    #sends data to the html template where it is displayed to user
    return render_template("./demo.html", players=queriedPlayers, numPlayers=queriedResult[0], numTournaments = queriedResult[1], numSets = queriedResult[2], tournaments = tournaments)

@app.route("/home")
def landing():
    namelogov3Ratio = 4.253392812
    namelogov4Ratio = 1.904075714

    return render_template("./home.html", width=250*namelogov3Ratio, height=250)



#runs on localhost, provides a port
app.run(host="0.0.0.0", port=5027)
