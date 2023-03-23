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
@app.route('/restaurants/<int:id>', methods = ['GET', 'DELETE'])
def restaurant_by_id(id):

    if request.method == 'GET':
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
    
    elif request.method == 'DELETE':
        restaurant = Restaurant.query.filter_by(id = id).first()
        if not restaurant:
            response = make_response(
                {"error" : "Restaurant not found"},
                404
            )
            return response
        
        else:
            db.session.delete(restaurant)
            db.session.commit()

            response = make_response(
                { "success" : "Deleted Restaurant"},
                200
            )
            return response      

#PIZZA GET
@app.route('/pizzas', methods = ['GET'])
def pizzas():
    pizzas_dict = [pizza.to_dict() for pizza in Pizza.query.all()]

    response = make_response(
        jsonify(pizzas_dict),
        200
    )
    return response

#POST Restaurant pizzas
@app.route('/restaurant_pizzas', methods = ['POST'])
def post_restaurant_pizzas():
    try:
        new_restaurant_pizza = RestaurantPizza(
            price = request.get_json()['price'],
            pizza_id = request.get_json()['pizza_id'],
            restaurant_id = request.get_json()['restaurant_id']
        )

        db.session.add(new_restaurant_pizza)
        db.session.commit()

        restaurant_pizza_dict = new_restaurant_pizza.pizza.to_dict(rules = ('restaurant_pizzas',))

        response = make_response(
            jsonify(restaurant_pizza_dict),
            201
        )

    except ValueError:

        response = make_response(
            { "errors": ["validation errors"]}
        )
    return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)

