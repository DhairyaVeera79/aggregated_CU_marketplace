from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
import base64
from redis import Redis
import json
import logging

app = Flask(__name__)

# Configure PostgreSQL database connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://dhairyaveera:password@34.83.67.63:5432/cu_marketplace'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Set the secret key for session management
app.secret_key = os.urandom(24)

# Initialize the SQLAlchemy object
db = SQLAlchemy(app)

# Initialize Redis
redis = Redis(host='127.0.0.1', port=6379)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Define the Item model
class Item(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    brand = db.Column(db.String(100))
    condition = db.Column(db.String(50))
    price = db.Column(db.Numeric(10, 2))
    image_data = db.Column(db.Text)  # Store image as Base64 encoded string
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f'<Item {self.item_name}>'

# Function to process messages from Redis
def process_redis_messages():
    pubsub = redis.pubsub()
    pubsub.subscribe('frontend_to_backend')

    for message in pubsub.listen():
        if message['type'] == 'message':
            data = json.loads(message['data'])
            logging.info(f"Received message: {data}")
            if data['action'] == 'add_item':
                add_item_to_db(data['item'])
            elif data['action'] == 'get_items':
                send_items_to_frontend()

# Function to add item to the database
def add_item_to_db(item_data):
    logging.info(f"Adding item to database: {item_data}")
    new_item = Item(
        item_name=item_data['item_name'],
        description=item_data['description'],
        brand=item_data['brand'],
        condition=item_data['condition'],
        price=item_data['price'],
        image_data=item_data['image_data']
    )
    db.session.add(new_item)
    db.session.commit()
    logging.info("Item added to database")

# Function to send items to the frontend
def send_items_to_frontend():
    with app.app_context():
        items = Item.query.all()
        items_list = [{"id": item.id, "item_name": item.item_name, "description": item.description, "brand": item.brand, "condition": item.condition, "price": str(item.price), "image_data": item.image_data} for item in items]
        redis.publish('backend_to_frontend', json.dumps(items_list))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables if they don't exist
        process_redis_messages()
    app.run(debug=True, host='0.0.0.0', port=5003)