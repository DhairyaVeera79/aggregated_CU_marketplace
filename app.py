# app.py
from flask import Flask, render_template, request, jsonify, abort

app = Flask(__name__)

# Sample static items with unique IDs
items = [
    {
        'id': 0,
        'name': 'Laptop',
        'description': 'Dell XPS 13, 8GB RAM, 256GB SSD',
        'price': 800,
        'image': 'sample.jpg'
    },
    {
        'id': 1,
        'name': 'Bicycle',
        'description': 'Mountain bike, lightly used',
        'price': 150,
        'image': 'sample.jpg'
    },
    {
        'id': 2,
        'name': 'Textbooks Bundle',
        'description': 'Collection of required textbooks for Fall semester',
        'price': 100,
        'image': 'sample.jpg'
    },
    {
        'id': 3,
        'name': 'Desk Chair',
        'description': 'Ergonomic office chair with lumbar support',
        'price': 120,
        'image': 'sample.jpg'
    },
    {
        'id': 4,
        'name': 'Smartphone',
        'description': 'iPhone 12, 64GB, good condition',
        'price': 600,
        'image': 'sample.jpg'
    },
    {
        'id': 5,
        'name': 'Guitar',
        'description': 'Acoustic guitar with a hard case',
        'price': 200,
        'image': 'sample.jpg'
    },
    {
        'id': 6,
        'name': 'Bookshelf',
        'description': 'Wooden bookshelf with 5 shelves',
        'price': 90,
        'image': 'sample.jpg'
    },
    {
        'id': 7,
        'name': 'Headphones',
        'description': 'Noise-cancelling over-ear headphones',
        'price': 150,
        'image': 'sample.jpg'
    },
]

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/database')
def database():
    return render_template('database.html', items=items)

@app.route('/sell', methods=['GET', 'POST'])
def sell():
    if request.method == 'POST':
        # Handle form submission
        item_name = request.form.get('item_name')
        brand = request.form.get('brand')
        age = request.form.get('age')
        price = request.form.get('price')
        image = request.files.get('image')
        
        # Here, you would process and save the data to the database and handle the image upload
        # For demonstration, we'll print the received data
        print(f"Item Name: {item_name}")
        print(f"Brand: {brand}")
        print(f"Age: {age} months")
        print(f"Price: ${price}")
        if image:
            image.save(f"static/images/{image.filename}")
            print(f"Image saved as {image.filename}")
            # Optionally, append the new item to the items list with a new id
            new_id = len(items)
            new_item = {
                'id': new_id,
                'name': item_name,
                'description': f"{brand}, {age} months old",
                'price': price,
                'image': image.filename
            }
            items.append(new_item)
        
        # Redirect or render a success message
        return render_template('sell.html', success=True)
    
    return render_template('sell.html')

# Route for item detail page
@app.route('/item/<int:item_id>')
def item_detail(item_id):
    # Find the item with the given id
    item = next((item for item in items if item['id'] == item_id), None)
    if item is None:
        abort(404)
    # Placeholder seller email
    seller_email = 'jesus.portilla@colorado.edu'
    return render_template('item_detail.html', item=item, seller_email=seller_email)

# Placeholder route for chatbot responses (for future integration)
@app.route('/chatbot/respond', methods=['POST'])
def chatbot_respond():
    user_message = request.json.get('message')
    # Here, you would integrate with OpenAI API to generate responses
    # For now, we'll return a placeholder response
    response = "This is a placeholder response."
    return jsonify({'response': response})

# 404 Error Handler
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
