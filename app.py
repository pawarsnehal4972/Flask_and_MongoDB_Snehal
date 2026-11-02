"""
Flask + MongoDB Atlas assignment
Author: Snehal

Task 1 : /api  -> reads a JSON list from data.json (backend file) and returns it
Task 2 : /form -> HTML form; on submit the data is inserted into MongoDB Atlas
                  * success -> redirect to /success  ("Data submitted successfully")
                  * error   -> same page is re-rendered with the error (no redirect)
"""
import json
import os
from datetime import datetime, timezone

from dotenv import load_dotenv
from flask import Flask, jsonify, redirect, render_template, request, url_for
from pymongo import MongoClient
from pymongo.errors import PyMongoError

load_dotenv()  # loads MONGO_URI etc. from the .env file

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "data.json")

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME", "flask_assignment")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "submissions")


def get_collection():
    """Create a MongoDB Atlas connection and return the collection.
    Raises an error (caught in the route) if the URI is missing or Atlas is unreachable."""
    if not MONGO_URI:
        raise RuntimeError("MONGO_URI is not set. Add it to the .env file.")
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    client.admin.command("ping")  # forces a real connection test
    return client[DB_NAME][COLLECTION_NAME]


# ------------------------------------------------------------------ Home
@app.route("/")
def home():
    return render_template("index.html")


# ------------------------------------------------- Task 1 : JSON API route
@app.route("/api")
def api():
    """Read the list stored in data.json and send it back as JSON."""
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return jsonify(data)
    except FileNotFoundError:
        return jsonify({"error": "data.json file not found"}), 404
    except json.JSONDecodeError:
        return jsonify({"error": "data.json contains invalid JSON"}), 500


# ------------------------------------- Task 2 : form  ->  MongoDB Atlas
@app.route("/form", methods=["GET", "POST"])
def form():
    if request.method == "GET":
        return render_template("form.html", error=None, values={})

    values = {
        "name": request.form.get("name", "").strip(),
        "email": request.form.get("email", "").strip(),
        "message": request.form.get("message", "").strip(),
    }

    # Basic validation
    if not values["name"] or not values["email"] or not values["message"]:
        return render_template(
            "form.html", error="All fields are required.", values=values
        ), 400
    if "@" not in values["email"] or "." not in values["email"].split("@")[-1]:
        return render_template(
            "form.html", error="Please enter a valid email address.", values=values
        ), 400

    try:
        collection = get_collection()
        collection.insert_one({**values, "submitted_at": datetime.now(timezone.utc)})
    except (PyMongoError, RuntimeError) as exc:
        # ERROR: stay on the same page and show the message (no redirect)
        return render_template(
            "form.html", error=f"Could not save data: {exc}", values=values
        ), 500

    # SUCCESS: redirect to another page
    return redirect(url_for("success"))


@app.route("/success")
def success():
    return render_template("success.html", message="Data submitted successfully")


if __name__ == "__main__":
    app.run(debug=True)
