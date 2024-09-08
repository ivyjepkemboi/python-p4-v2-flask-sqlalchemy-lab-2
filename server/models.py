from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy

db = SQLAlchemy()

class Customer(db.Model, SerializerMixin):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    reviews = db.relationship('Review', back_populates='customer', lazy='subquery')
    items = association_proxy('reviews', 'item')  # Association proxy to access items

    # Adjust serialization rules to include reviews for testing
    serialize_rules = ('-reviews.customer',)  

    def __repr__(self):
        return f'<Customer {self.id}, {self.name}>'

class Item(db.Model, SerializerMixin):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Float)
    reviews = db.relationship('Review', back_populates='item', lazy='subquery')

    # Adjust serialization rules to include reviews for testing
    serialize_rules = ('-reviews.item',) 

    def __repr__(self):
        return f'<Item {self.id}, {self.name}, {self.price}>'

class Review(db.Model, SerializerMixin):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer)
    comment = db.Column(db.String)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))
    customer = db.relationship('Customer', back_populates='reviews', lazy='select')
    item = db.relationship('Item', back_populates='reviews', lazy='select')

    # Adjust serialization rules to include customer and item for testing
    serialize_rules = ('-customer.reviews', '-item.reviews',)  

    def __repr__(self):
        return f'<Review {self.id}, {self.rating}, {self.comment}>'
