from pymongo.mongo_client import MongoClient
import os
from dotenv import load_dotenv
import urllib.parse

# Load environment variables from .env file
load_dotenv()

# Access the ENV
_username = os.getenv("USERNAME", "")
_password = os.getenv("PASSWORD", "")

username = urllib.parse.quote_plus(_username)
password = urllib.parse.quote_plus(_password)

uri = ("mongodb+srv://%s:%s@cluster0.pwizjjp.mongodb.net/?retryWrites=true&w=majority" % (username, password))
# Create a new client and connect to the server
client = MongoClient(uri, ssl=True)

#Database 
db = client.gpx

#Table
gpx_enabled = db.gpx_enabled



