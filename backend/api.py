import urllib
import os
import json
from bson import ObjectId

from flask import Flask, jsonify, request, Response
from flask_cors import CORS
from dotenv import load_dotenv
from pymongo import MongoClient
from better_profanity import profanity

# Load environment variables from our .env file
load_dotenv()

# Declare a new instance of a Flask application
app = Flask(__name__)
CORS(app)

"""
Flask is a web framework for Python that allows us to run simple web servers.
We can make use of flasks's routing to create an API that allows us to talk to MongoDB
using only HTTP requests.

Let's define a few "routes", or URL patterns, that allow us to get, modify, and delete messages.
Based on the HTTP Request method and the route, we define actions that our API can take to alter data
for us.
"""

# We are using Flask to write our API. Flask is a Python web framework that allows us to
# associate python methods with url endpooints. When a user hits a route
# that matches a url pattern, the corresponding python method is called.
@app.route("/welcome")
def get_text():
    # This is a basic method that returns the text "Hello, world!" when
    # a user goes to http://<our-domain>/welcome
    return "Hello, world!"


@app.route("/welcome/<text>")
def get_custom_text(text):
    # In Flask, we can also capture variables that are stored in our url.
    # When a user visits "/welcome/<text>", this endpoint will return
    # everything after the second "/" as text.
    return text


"""
Now, we can move on to the guts of our API: actually interacting with our database.
"""

# Establish a connection to our MongoDB database

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

# To interact with our messages, let's define a "/messages"
# route. A "GET" request to this endpoint will return all messages in the database.
# A "POST" request will insert a new message.
@app.route("/messages", methods=["GET", "POST"])
def get_messages():
    if request.method == "GET":
        # (Web Browsers perform a GET request when you enter a URL into the search bar)
        # Return a list of all documents in the "messages" collection.
        return jsonify([x for x in db[collection].find()])
    elif request.method == "POST":
        # Get data from our request
        data = request.json
        # Construct a new dictionary with an "author" and "content" properties.
        new_message = censor_values(
            {"author": data["author"], "content": data["content"]}
        )
        # Insert new message
        db[collection].insert_one(new_message)
        # Return the newly inserted message
        return jsonify(new_message)
    
    return Response("Invalid method", status=400)


# Now, let's say we want to interact with a single message.
# Let's define the URL route "/messages/<id>" that will
# allow us to interact with messages with a particular id.
@app.route("/messages/<id>", methods=["GET", "PUT", "DELETE"])
def get_message(id):
    # First, try to find a message with this ID.
    message = db[collection].find_one({"_id": ObjectId(id)})

    if not message:
        # If we cannot find a message with this ID, return a 404 status code.
        return Response("404 Not Found", status=404)

    if request.method == "GET":
        # Get a message with a particular ID
        return message

    elif request.method == "PUT":
        # Modify a message with a particular ID
        new_message_fields = censor_values(request.json)
        # Find this message document in db and update it
        updated = db[collection].find_one_and_update(
            {"_id": ObjectId(id)}, {"$set": new_message_fields}
        )
        return jsonify(updated)

    elif request.method == "DELETE":
        # Delete a message with a particular ID
        deleted = db[collection].find_one_and_delete({"_id": ObjectId(id)})
        return jsonify(deleted)

    return Response("Invalid method", status=400)


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
