import os
import click
from flask import Flask, abort, jsonify, render_template, request

from werkzeug.exceptions import HTTPException
from .db import Database
from .logic import (
    ACTIVITY_MULTIPLIERS,
    calculate_bmi,
    calculate_calories,
    get_bmi_category,
)

# Use an environment variable for the database path, defaulting to a local file.
# In Azure App Service, set an App Setting for 'DATABASE_PATH' to a persistent
# location like '/home/data/fitness.db'.
DB_FILE = os.environ.get("DATABASE_PATH", "fitness.db")
app = Flask(__name__)

# Ensure the database is initialized when the app starts
with Database(DB_FILE) as db:
    db.initialize_db()

@app.cli.command("init-db")
def init_db_command():
    """Clear existing data and create new tables."""
    with Database(DB_FILE) as db:
        db.initialize_db()
    print("Initialized the database.")


@app.cli.command("calculate")
@click.argument("name")
@click.option("--weight", type=float, required=True, help="Weight in kilograms.")
@click.option("--height", type=float, required=True, help="Height in meters.")
@click.option("--age", type=int, required=True, help="Age in years.")
@click.option(
    "--gender",
    type=click.Choice(["male", "female"]),
    required=True,
    help='Gender: "male" or "female".',
)
@click.option(
    "--activity",
    type=click.Choice(ACTIVITY_MULTIPLIERS.keys()),
    required=True,
    help="Your daily activity level.",
)
def calculate_command(name, weight, height, age, gender, activity):
    """Calculate health metrics and save the record."""
    print("\n--- Health Metrics Calculation ---")
    try:
        bmi = calculate_bmi(weight, height)
        bmi_category = get_bmi_category(bmi)
        print(f"BMI: {bmi:.2f} ({bmi_category})")

        calories = calculate_calories(weight, height, age, gender, activity)
        print(f"Estimated Daily Calorie Needs: {calories:.2f} kcal")

        with Database(DB_FILE) as db:
            db.save_record(
                name, age, weight, height * 100, activity, bmi, calories
            )
        print(f"\nSuccessfully saved record for {name}.")
    except ValueError as e:
        print(f"\nError: {e}")


@app.cli.command("show-records")
def show_records_command():
    """List all saved fitness records."""
    print("\n--- Saved Fitness Records ---")
    with Database(DB_FILE) as db:
        records = db.fetch_all_records()
        if records:
            print(
                f"{'ID':<4} {'Name':<20} {'Age':<5} {'Weight':<8} {'Height':<8}"
                f" {'BMI':<6} {'Calories':<10}"
            )
            print("-" * 70)
            for r in records:
                height_in_m = r["height"] / 100.0
                print(
                    f"{r['id']:<4} {r['name']:<20} {r['age']:<5} {r['weight']:<8.1f}"
                    f" {height_in_m:<8.2f} {r['bmi']:<6.2f} {r['calories']:<10.2f}"
                )
        else:
            print("No records found in the database.")

@app.errorhandler(HTTPException)
def handle_http_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = jsonify(
        code=e.code, name=e.name, description=e.description
    ).data
    response.content_type = "application/json"
    return response
@app.route('/')
def home():
    return render_template("index.html")

@app.route('/register', methods=['POST'])
def register():
    data = request.form
    required_fields = ['name', 'age', 'weight', 'height', 'gender', 'activity']

    if not all(field in data for field in required_fields):
        abort(400, description="Missing one or more required fields.")

    try:
        name = data['name']
        age = int(data['age'])
        weight = float(data['weight'])
        height_cm = float(data['height'])
        gender = data['gender']
        activity = data['activity']

        if gender not in ['male', 'female']:
            abort(400, description=f"Invalid value for gender: '{gender}'.")

        if activity not in ACTIVITY_MULTIPLIERS:
            abort(400, description=f"Invalid value for activity: '{activity}'.")
    except (TypeError, ValueError):
        abort(400, description="Invalid data type for one or more fields.")

    try:
        height_m = height_cm / 100.0
        bmi = calculate_bmi(weight, height_m)
        calories = calculate_calories(weight, height_m, age, gender, activity)
    except ValueError as e:
        abort(400, description=str(e))

    with Database(DB_FILE) as db:
        db.save_record(name, age, weight, height_cm, activity, bmi, calories)

    return jsonify({
        'name': name,
        'bmi': f"{bmi:.2f}",
        'calories': f"{calories:.2f}"
    })

@app.route('/records', methods=['GET'])
def records():
    with Database(DB_FILE) as db:
        rows = db.fetch_all_records()

    return jsonify([dict(row) for row in rows])

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)