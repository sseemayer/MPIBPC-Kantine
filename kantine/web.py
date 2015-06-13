import os
import datetime

from flask import Flask, request, redirect, url_for, jsonify

from kantine.database import session
from kantine.models import Meal

app = Flask(__name__)

@app.route("/")
def home():
    return "Nothing to see here yet, move along"


@app.route("/api/meals")
def next_meals():
    upcoming_meals = session.query(Meal).filter(Meal.date >= datetime.datetime.now().date()).order_by(Meal.date).all()

    return jsonify(meals=[
        {
            "date": m.date.isoformat(),
            "type": m.mealtype,
            "name_de": m.name,
            "name_en": m.name_en
        }
        for m in upcoming_meals
    ])
