from flask import Flask, render_template, redirect, url_for, request, jsonify
import os
from redis import Redis
import json
import base64

app = Flask(__name__)

# Set the secret key for session management
app.secret_key = os.urandom(24)

# Initialize Redis
redis = Redis(host='localhost', port=6379, db=0)

# Home route
@app.route('/')
def home():
    return render_template('home.html')

# Database route
@app.route('/database')
def database():
    return render_template('database.html')

# Sell route
@app.route('/sell', methods=['GET', 'POST'])
def sell():
    if request.method == 'POST':
        # Get form data
        item_name = request.form['item_name']
        description = request.form['description']
        brand = request.form['brand']
        condition = request.form['condition']
        price = request.form['price']
        file = request.files['image']
        image_data = base64.b64encode(file.read()).decode('utf-8')

        # Publish item data to Redis
        item_data = {
            'action': 'add_item',
            'item': {
                'item_name': item_name,
                'description': description,
                'brand': brand,
                'condition': condition,
                'price': price,
                'image_data': image_data
            }
        }
        redis.publish('frontend_to_backend', json.dumps(item_data))
        return redirect(url_for('database'))

    return render_template('sell.html')

# API endpoint to fetch items from Redis
@app.route('/api/items', methods=['GET'])
def get_items():
    redis.publish('frontend_to_backend', json.dumps({'action': 'get_items'}))
    pubsub = redis.pubsub()
    pubsub.subscribe('backend_to_frontend')

    for message in pubsub.listen():
        if message['type'] == 'message':
            items = json.loads(message['data'])
            return jsonify(items)

if __name__ == '__main__':
    app.run(debug=True, port=5002)