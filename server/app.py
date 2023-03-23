#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Restaurant, RestaurantPizza, Pizza

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)

@app.route('/')
def index():
    return '<h1>Code challenge</h1>'

#my routes start here
@app.route('/restaurants', methods = ['GET'])
def restaurants():
    restaurants_dict = [restaurant.to_dict() for restaurant in Restaurant.query.all()]

    response = make_response(
        jsonify(restaurants_dict),
        200
    )
    return response

#Restaurant by Id
@app.route('/restaurants/<int:id>', methods = ['GET'])
def restaurant_by_id(id):

    restaurant = Restaurant.query.filter_by(id = id).first()
    if restaurant:

        restaurant_dict = restaurant.to_dict()
        response = make_response(
            jsonify(restaurant_dict),
            200
        )
    else:
        response = make_response(
            {"error" : "Restaurant not found"}
        )
    return response


if __name__ == '__main__':
    app.run(port=5555, debug=True)
