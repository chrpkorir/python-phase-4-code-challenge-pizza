#!/usr/bin/env python3
from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, jsonify, make_response
from flask_restful import Api, Resource
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)


@app.route("/")
def index():
    return "<h1>Code challenge</h1>"

# Fetches all restaurants
@app.route('/restaurants', methods=['GET'])
def get_restaurants():
    restaurants = Restaurant.query.all()
    return jsonify([restaurant.to_dict() for restaurant in restaurants])

# Fetches restaurants by ID
@app.route('/restaurants/<int:id>', methods=['GET'])
def get_restaurant_by_id(id):
    # Query the restaurant by ID
    restaurant = Restaurant.query.get(id)
    if not restaurant:
         return jsonify({"error": "Restaurant not found"}), 404

    # Return the restaurant data in the specified format
    return jsonify(restaurant.to_dict())

@app.route('/restaurants/<int:id>', methods=['DELETE'])
def del_restaurant(id):
    restaurant = db.session.get(Restaurant, id)
    if not restaurant:
        return jsonify({"error": "Restaurant not found"}), 404
    
    db.session.delete(restaurant)
    db.session.commit()
    return make_response('', 204)

@app.route('/pizzas', methods=['GET'])
def get_pizza():
    pizzas = Pizza.query.all()
    return jsonify([pizza.to_dict(rules=('-restaurant_pizzas',)) for pizza in pizzas])

@app.route('/restaurant_pizzas', methods=['POST'])
def create_restaurant_pizza():
    try:
        data = request.get_json()
        
        if not all(field in data for field in ['price', 'pizza_id', 'restaurant_id']):
            return jsonify({"errors": ["validation errors"]}), 400
        
        restaurant_pizza = RestaurantPizza(
            price=data['price'],
            pizza_id=data['pizza_id'],
            restaurant_id=data['restaurant_id']
        )
        
        db.session.add(restaurant_pizza)
        db.session.commit()
        return jsonify(restaurant_pizza.to_dict()), 201
    
    except ValueError:
        return jsonify({"errors": ["validation errors"]}), 400
    except Exception:
        return jsonify({"errors": ["validation errors"]}), 400

if __name__ == "__main__":
    app.run(port=5555, debug=True)
