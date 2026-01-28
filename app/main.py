import flask
import json
from flask import Flask, request, render_template_string, render_template

app = Flask(__name__)

# Global cars data
cars = []

def load_cars():
    """Load cars from JSON file into global cars list"""
    global cars
    with open('cars.json', 'r') as f:
        cars = json.load(f)

# Initialize cars data on startup
load_cars()

# ---------------- Root Route ----------------
@app.route("/")
def index():
    return render_template('index.html')

# ---------------- Cars Route ----------------
@app.route("/api/cars")
def get_cars():
    return flask.jsonify(cars)

@app.route("/api/cars/<int:id>")
def get_car_by_id(id):
    for car in cars:
        if car['carid'] == id:
            return flask.jsonify(car)
    return flask.jsonify({"error": "Car not found"}), 404

@app.route("/api/cars/save", methods=['POST'])
def save_car():
    new_car = request.get_json()
    # Convert carid to int for comparison
    new_car['carid'] = int(new_car['carid'])
    
    for i, car in enumerate(cars):
        if car['carid'] == new_car['carid']:
            cars[i] = new_car
            return flask.jsonify({"message": "Car updated successfully"}), 200 
            
    return flask.jsonify({"error": "Car not found"}), 404

@app.route("/api/cars/search", methods=['POST'])
def search_cars():
    criteria = request.get_json()
    title = criteria.get('title', '').lower()
    
    filtered_cars = [
        car for car in cars
        if (title in car['title'].lower() if title else True)
    ]
    
    return flask.jsonify(filtered_cars)

if __name__ == "__main__":
    # Development server — use `flask run` or a production server for deployment
    app.run(debug=True, host="0.0.0.0", port=5000)

