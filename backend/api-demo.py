import urllib
import os
import json
from bson import ObjectId

from flask import Flask, jsonify, request, Response
from flask_cors import CORS
from dotenv import load_dotenv
from pymongo import MongoClient
from better_profanity import profanity
from pyparsing import col

# Load environment variables from our .env file
load_dotenv()

# Declare a new instance of a Flask application
app = Flask(__name__)
CORS(app)

# We are using Flask to write our API. Flask is a Python web framework that allows us to
# associate python methods with url endpooints. When a user hits a route
# that matches a url pattern, the corresponding python method is called.
@app.route("/welcome")
def get_text():
    # This is a basic method that returns the text "Hello, world!" when
    # a user goes to http://<our-domain>/welcome
    # TODO: Implement Me!
    pass


@app.route("/welcome/<text>")
def get_custom_text(text):
    # In Flask, we can also capture variables that are stored in our url.
    # When a user visits "/welcome/<text>", this endpoint will return
    # everything after the second "/" as text.
    # TODO: Implement Me!
    pass


# This connection string tells the MongoDB Client which database to connect to in the cloud.
# Remember, a client is a service that talks to technologies on the web.
# It is username/password protected.
CONN_STR = f"mongodb+srv://mongouser:{urllib.parse.quote_plus(os.environ['MONGO_PASSWORD'])}@cluster0.4xnby.mongodb.net/postit?retryWrites=true&w=majority"

# Initialize a new MongoClient() with our connection string.
client = MongoClient(CONN_STR)

# Our database is a property of the connection to our client.
# We can now use this database connection to read, write, edit, and delete documents.
db = client["postit"]

# Our collection is called "messages", let's save this as a global variable for future use.
collection = "messages"


@app.route("/messages")
def handle_messages():
    # GET: Get all messages from MongoDB
    # POST: Write a new message to the database.

    # TODO: Implement Me!
    pass


# # # #
# < Ignore this section >
# # # #
class JSONEncoder(json.JSONEncoder):
    """
    We create our own JSONEncoder to handle MongoDB IDs of type ObjectId
    when serializing objects.
    """

    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


app.json_encoder = JSONEncoder


def censor_values(message):
    if type(message) == str:
        return profanity.censor(message)
    elif type(message) == dict:
        return {k: profanity.censor(v) for k, v in message.items()}
    else:
        # Not sure how to censor this object.
        print(f"[ WARNING ]: Cannot censor object of type {type(message)}")
        return message


# # # #
# < Ignore this section >
# # # #


if __name__ == "__main__":
    app.run(port=5000)

