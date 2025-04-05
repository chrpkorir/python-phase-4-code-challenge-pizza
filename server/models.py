from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(
    naming_convention={
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    }
)

db = SQLAlchemy(metadata=metadata)


class Restaurant(db.Model, SerializerMixin):
    __tablename__ = "restaurants"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    address = db.Column(db.String)

    
    # Establishing the many-to-many relationship
    pizzas = db.relationship('Pizza', secondary='restaurant_pizzas', back_populates='restaurants', cascade="all, delete")
    # add serialization rules
    serialize_rules = ('-restaurant_pizzas.restaurant', '-pizzas.restaurant_pizzas')

    def __repr__(self):
        return f"<Restaurant {self.name}>"


class Pizza(db.Model, SerializerMixin):
    __tablename__ = "pizzas"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    ingredients = db.Column(db.String)

    # add relationship
    restaurant_pizzas = db.relationship('RestaurantPizza', back_populates='pizza')
    #restaurants = association_proxy('restaurant_pizzas', 'restaurant')

    # add serialization rules
    serialize_rules = ('-restaurant_pizzas.pizza', '-restaurants.restaurant_pizzas')
    def __repr__(self):
        return f"<Pizza {self.name}, {self.ingredients}>"


class RestaurantPizza(db.Model, SerializerMixin):
    __tablename__ = "restaurant_pizzas"

    # Define the primary key for this join table
    id = db.Column(db.Integer, primary_key=True)

    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), primary_key=True)
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizzas.id'), primary_key=True)
    price = db.Column(db.Integer, nullable=False)

    # To define relationship
    restaurant = db.relationship('Restaurant', back_populates='pizzas')
    pizza = db.relationship('Pizza', back_populates='restaurants')
    # add serialization rules
    serialize_rules = ('-pizza.restaurant_pizzas', '-restaurant.restaurant_pizzas')
    # add validation
    @validates('price')
    def prce_validate(self, key, price):
        if not 1 <= price <= 30:
            raise ValueError("price shuld be between 1 and 30")
        return price
    def __repr__(self):
        return f"<RestaurantPizza ${self.price}>"
