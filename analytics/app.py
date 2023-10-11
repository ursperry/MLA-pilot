from dotenv import load_dotenv
from flask import Flask, render_template, jsonify
from pymongo import MongoClient
from flask_pymongo import PyMongo
from flask_cors import CORS
from urllib.parse import quote_plus
from bson import json_util
import traceback
import os
import config

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}},
     methods="GET,HEAD,POST,OPTIONS,PUT,PATCH,DELETE")

load_dotenv()
title = "Weekly Exercise Tracker Statistics"
heading = "MLA Flask Microservice"
user = "testuser"

client = MongoClient(config.MONGO_URI)
db = client.test


@app.route('/')
def index():
    exercises = db.exercises.find()
    exercises_list = list(exercises)

    return json_util.dumps(exercises_list)


@app.route('/stats')
def stats():
    pipeline = [
        {"$match": {"username": user}},
        {"$group": {
            "_id": "$exerciseType",
            "duration": {"$sum": "$duration"}
        }}
    ]

    stats = list(db.exercises.aggregate(pipeline))
    return jsonify(stats=stats)


@app.route("/list")
def lists():
    exercises = db.exercises.find()
    return render_template('index.html', activities=exercises, t=title, h=heading)


@app.errorhandler(Exception)
def handle_error(e):
    app.logger.error(f"An error occurred: {e}")
    traceback.print_exc()
    return jsonify(error="An internal error occurred"), 500


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5050)
