from flask import Flask, request, jsonify, render_template_string
from logic import calculate_bmi, calculate_calories
from db import init_db, save_record, fetch_all_records

app = Flask(__name__)
init_db() # ensure DB exists when app starts

INDEX_HTML = """
<!doctype html>
<title>Fitness Tracker</title>
<h1>Fitness Tracker</h1>
<form action="/register" method="post">
  Name: <input name="name"><br>
  Age: <input name="age" type="number"><br>
  Weight (kg): <input name="weight" type="number" step="0.1"><br>
  Height (cm): <input name="height" type="number" step="0.1"><br>
  Gender:
  <select name="gender">
    <option value="male">Male</option>
    <option value="female">Female</option>
  </select><br>
  Activity Level:
  <select name="activity">
    <option value="sedentary">Sedentary (little or no exercise)</option>
    <option value="light">Light (1-3 days/week)</option>
    <option value="moderate">Moderate (3-5 days/week)</option>
    <option value="active">Active (6-7 days/week)</option>
    <option value="very_active">Very Active (hard exercise/job)</option>
  </select><br>
  <button type="submit">Register & Calculate</button>
</form>
<p><a href="/records">View saved records</a></p>
"""

@app.route('/')
def home():
    return render_template_string(INDEX_HTML)

@app.route('/register', methods=['POST'])
def register():
    name = request.form.get('name')
    age = int(request.form.get('age'))
    weight = float(request.form.get('weight'))
    height_cm = float(request.form.get('height'))
    gender = request.form.get('gender').lower()
    activity = request.form.get('activity').lower()

    # BMI expects height in meters
    height_m = height_cm / 100.0
    bmi = calculate_bmi(weight, height_m)

    # Calories expects height in cm
    calories = calculate_calories(weight, height_cm, age, gender, activity)

    save_record(name, age, weight, height_cm, activity, bmi, calories)
    return jsonify({'name': name, 'bmi': bmi, 'calories': calories})

@app.route('/records', methods=['GET'])
def records():
    rows = fetch_all_records()
    # return JSON for simplicity
    return jsonify([{
        'id': r[0], 'name': r[1], 'age': r[2], 'weight': r[3],
        'height': r[4], 'activity': r[5], 'bmi': r[6], 'calories': r[7]
    } for r in rows])

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)