import os
import collections
import datetime
import humanize

from flask import Flask, request, redirect, url_for, jsonify, send_from_directory, render_template

from kantine.database import session
from kantine.models import Meal

static_folder = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "static")

app = Flask(__name__, static_folder=static_folder, template_folder=static_folder)

@app.route("/")
def home():


    upcoming_meals = session.query(Meal).filter(Meal.date >= datetime.datetime.now().date()).order_by(Meal.mealtype).order_by(Meal.date).all()

    type_to_human = {
        "meal1": "Option 1",
        "meal2": "Option 2",
        "wok_or_pasta": "Wok / Pasta",
        "special": "Special",
        "sides": "Extras"
    }

    meals_grouped = {}

    for m in upcoming_meals:
        ifmt = m.date.isoformat()
        if ifmt not in meals_grouped:
            meals_grouped[ifmt] = {
                "date": ifmt,
                "date_human": m.date.strftime("%A, %B %d"),
                "options": []
            }

        meals_grouped[ifmt]['options'].append({
            "type": m.mealtype,
            "type_human": type_to_human[m.mealtype],
            "name_de": m.name,
            "name_en": m.name_en
        })

    return render_template("index.html", meals=sorted(list(meals_grouped.values()), key=lambda d: d['date']))

@app.route("/favicon.ico")
def static_favicon():
    return app.send_static_file('favicon.ico')

@app.route("/images/<path:path>")
def static_image(path):
    return send_from_directory(os.path.join(static_folder, 'images'), path)

@app.route("/js/<path:path>")
def static_js(path):
    return send_from_directory(os.path.join(static_folder, 'js'), path)


@app.route("/css/<path:path>")
def static_css(path):
    return send_from_directory(os.path.join(static_folder, 'css'), path)


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


@app.teardown_request
def shutdown_session(exception=None):
    session.remove()
