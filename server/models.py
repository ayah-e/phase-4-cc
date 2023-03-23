from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

# Add models here

#Pizza model
class Pizza(db.Model, SerializerMixin):
    __tablename__ = 'pizzas'
#serialize rules
    serialize_rules = ("-restaurant_pizzas", "-created_at", "-updated_at")

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    ingredients= db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default= db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
#relationship
    restaurant_pizzas = db.relationship("RestaurantPizza", backref = "pizza")
#association proxy
    restaurants = association_proxy("restaurant_pizzas", "restaurant")


#Restaurant model
class Restaurant(db.Model, SerializerMixin):
    __tablename__ = 'restaurants'
#serialize rules
    serialize_rules = ("-restaurant_pizzas", "-created_at", "-updated_at")

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    address= db.Column(db.String)
#relationship
    restaurant_pizzas = db.relationship("RestaurantPizza", backref="restaurant")
#association proxy
    pizzas = association_proxy("restaurant_pizzas", "pizza")

#Restaurant Pizza model
class RestaurantPizza(db.Model, SerializerMixin):
    __tablename__ = 'restaurant_pizzas'
#serialize rules
    serialize_rules = ("-restaurant.restaurant_pizzas", "-pizza.restaurant_pizzas")

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default= db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    #foreign keys
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizzas.id'))
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'))

    #validations
    @validates("price")
    def validate_price(self, key, price):
        if price >= 1 and price <= 30:
            return price
        raise ValueError("invalid price")




