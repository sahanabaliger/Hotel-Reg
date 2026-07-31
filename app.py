from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-this-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Ensure instance folder exists (Flask uses this by default for the DB)
basedir = os.path.abspath(os.path.dirname(__file__))
instance_path = os.path.join(basedir, 'instance')
if not os.path.exists(instance_path):
    os.makedirs(instance_path)

db = SQLAlchemy(app)


# ---------------- MODEL ----------------
class Hotel(db.Model):
    __tablename__ = 'hotels'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    location = db.Column(db.String(120), nullable=False)
    rooms = db.Column(db.Integer, nullable=False)
    price_per_night = db.Column(db.Float, nullable=False)
    contact = db.Column(db.String(50), nullable=True)

    def __repr__(self):
        return f'<Hotel {self.name}>'


# Create tables if they don't already exist (won't overwrite existing db/table)
with app.app_context():
    db.create_all()


# ---------------- ROUTES ----------------

# READ - list all hotels
@app.route('/')
def index():
    hotels = Hotel.query.all()
    return render_template('index.html', hotels=hotels)


# CREATE - add a new hotel
@app.route('/add', methods=['POST'])
def add_hotel():
    name = request.form.get('name')
    location = request.form.get('location')
    rooms = request.form.get('rooms')
    price = request.form.get('price')
    contact = request.form.get('contact')

    if not name or not location or not rooms or not price:
        flash('Please fill in all required fields.', 'error')
        return redirect(url_for('index'))

    new_hotel = Hotel(
        name=name,
        location=location,
        rooms=int(rooms),
        price_per_night=float(price),
        contact=contact
    )
    db.session.add(new_hotel)
    db.session.commit()
    flash('Hotel registered successfully!', 'success')
    return redirect(url_for('index'))


# UPDATE - edit an existing hotel
@app.route('/update/<int:hotel_id>', methods=['POST'])
def update_hotel(hotel_id):
    hotel = Hotel.query.get_or_404(hotel_id)

    hotel.name = request.form.get('name')
    hotel.location = request.form.get('location')
    hotel.rooms = int(request.form.get('rooms'))
    hotel.price_per_night = float(request.form.get('price'))
    hotel.contact = request.form.get('contact')

    db.session.commit()
    flash('Hotel updated successfully!', 'success')
    return redirect(url_for('index'))


# DELETE - remove a hotel
@app.route('/delete/<int:hotel_id>')
def delete_hotel(hotel_id):
    hotel = Hotel.query.get_or_404(hotel_id)
    db.session.delete(hotel)
    db.session.commit()
    flash('Hotel deleted successfully!', 'success')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)