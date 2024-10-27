from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure PostgreSQL database connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://dhairyaveera@localhost/cu_marketplace'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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
        item_name = request.form['item_name']
        description = request.form['description']
        brand = request.form['brand']
        condition = request.form['condition']
        price = request.form['price']
        new_item = Item(user_id=1, item_name=item_name, description=description, brand=brand, condition=condition, price=price)
        db.session.add(new_item)
        db.session.commit()
        return redirect(url_for('database'))
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
