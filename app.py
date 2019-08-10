# Dependencies
from flask import Flask, render_template
import scrape_mars
import pymongo

app=Flask(__name__)

conn = 'mongodb://localhost:27017'

client = pymongo.MongoClient(conn)

db= client.team_db

