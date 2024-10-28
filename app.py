from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
import os  # Import os to use os.urandom for generating a random secret key
from werkzeug.utils import secure_filename  # Add this import for file handling



app = Flask(__name__)

# Configure PostgreSQL database connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://dhairyaveera@localhost/cu_marketplace'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Set the secret key for session management
app.secret_key = os.urandom(24)  # Generates a random secret key

# Set the maximum content length for uploads (16 MB)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limit to 16 MB

# Initialize the SQLAlchemy object
db = SQLAlchemy(app)

# Define the User model
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True, nullable=False)
    identikey = db.Column(db.String(50), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.name}>'

# Define the Item model
class Item(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    item_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    brand = db.Column(db.String(100))
    condition = db.Column(db.String(50))
    price = db.Column(db.Numeric(10, 2))
    image_url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f'<Item {self.item_name}>'

# Home route
@app.route('/')
def home():
    return render_template('home.html')

# Database route
@app.route('/database')
def database():
    items = Item.query.all()  # Fetch all items from the database
    return render_template('database.html', items=items)

# Sell route
@app.route('/sell', methods=['GET', 'POST'])
def sell():
    if request.method == 'POST':
        # Handle image upload
        if 'image' not in request.files:
            flash('No file part')
            return redirect(url_for('sell'))
        file = request.files['image']
        if file.filename == '':
            flash('No selected file')
            return redirect(url_for('sell'))

        # Get form data
        item_name = request.form['item_name']
        description = request.form['description']
        brand = request.form['brand']
        condition = request.form['condition']
        price = request.form['price']

        # Image filename
        filename = secure_filename(file.filename)
        print(f"Image file received: {filename}")

        # Save the image file
        image_path = os.path.join('static/images', filename)

        try:
            file.save(image_path)  # Save the image
            print(f"Image saved to: {image_path}")  # Confirm save location
        except Exception as e:
            print(f"Error saving image: {e}")  # Catch save errors
            flash('An error occurred while saving the image.')
            return redirect(url_for('sell'))

        # Generate the URL for the image
        image_url = url_for('static', filename='images/' + filename)
        print(f"Image URL generated: {image_url}")

        # Create new item and add to the database
        new_item = Item(
            user_id=1,  # Replace with the actual user ID or logic for user assignment
            item_name=item_name,
            description=description,
            brand=brand,
            condition=condition,
            price=price,
            image_url=image_url
        )

        try:
            db.session.add(new_item)
            db.session.commit()
            print("Item added to database successfully.")
            flash('Item added successfully!')  # Flash a success message
        except Exception as e:
            db.session.rollback()
            print(f"Error occurred while adding to the database: {e}")
            flash('An error occurred while adding the item.')

        return redirect(url_for('database'))  # Redirect to the database view

    return render_template('sell.html')


# Item Details route
@app.route('/item/<int:item_id>')
def item_details(item_id):
    item = Item.query.get_or_404(item_id)
    return render_template('item_detail.html', item=item)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables if they don't exist
    app.run(debug=True)
