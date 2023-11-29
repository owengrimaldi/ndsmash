#!/usr/bin/env python3

'''
manualDB.py

This program contains the functions used to insert, update, and delete
different entries in the db. main() currently is pointless as it was used
as an initial barebones demo.

Also contains the queries for all searches or changes.

'''

from flask import Flask, render_template
from mysql.connector import connect, Error
from graphqlclient import GraphQLClient
import json, time, os

defaultPFP = "https://www.bing.com/th?pid=Sgg&qlt=100&u=https%3A%2F%2Fimages.start.gg%2Fimages%2Fuser%2F1620550%2Fimage-a007516ec2c2ce38b682771bcda1381b-optimized.png&ehk=UsRQKBt1XEhWGoWxWcP12zHe1dRm7XUNXGYGF5iqpmo%3D&w=160&h=160&r=0&c=3"

insertPlayer = "insert into players (id, pfp, username, prefix) VALUES (%s, %s, %s, %s)"
updatePlayer = "update players set %s = %s where %s = %s"
deletePlayer = "delete from players where players.id = %s"

insertSet = "insert into sets (id, eventID, winnerID, loserID, winnerScore, loserScore) VALUES (%s, %s, %s, %s, %s, %s)"
updateSet = "update sets set %s = %s where %s = %s"
deleteSet = "delete from sets where sets.id = %s"

insertTournament = "insert into tournaments (id, name, date, location, url, attendees) VALUES (%s, %s, %s, %s, %s, %s)"
updateTournament = "update tournaments set %s = %s where %s = %s"
deleteTournament = "delete from tournaments where tournaments.id = %s"

database = connect(host="localhost", user="ogrimald", password="goirish", database="ogrimald")
cursor = database.cursor(buffered=True)
cursor.execute("use ogrimald")

def main():

    ndQuery()
    insertQuery(insertPlayer, (6969, "http://dsg4.crc.nd.edu/wp/wp-content/uploads/2021/07/me_2019.jpeg", "Prof. Weninger", "ND")) 
    ndQuery()
    updateQuery(updatePlayer, ('id', 69, 'id', 6969))
    ndQuery()
    deleteQuery(deletePlayer, (69,))
    ndQuery()
    input("Press anything to exit...")

def ndQuery():
    cursor.execute("select username from players where players.prefix = 'ND'")
    queriedPlayers = [x[0] for x in cursor]
    print("Executing: select username from players where players.prefix = 'ND'")
    print(f"Results: {queriedPlayers}")

    cursor.execute("select * from players where players.id = 6969")
    for x in cursor:
        print(f"Player: {x}")
    print()

def insertQuery(query, values):
    try:
        cursor.execute(query, values)
        print(f"Inserting {values}...")
        database.commit()
    except:
        print(f"Error inserting!")
    print()

def deleteQuery(query, id):
    try:
        cursor.execute(query, id)
        print(f"Deleting with id: {id}...")
        database.commit()
    except:
        print(f"Error deleting!")
    print()

def updateQuery(query, values):
    try:
        query = query % values
        print(query)
        cursor.execute(query)
        print(f"Updating  with {values}...")
        database.commit()
    except:
        print(f"Error updating!")
    print()


if __name__ == '__main__':
    main()



