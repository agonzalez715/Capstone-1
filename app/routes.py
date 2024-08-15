from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash
from models import Car, db

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('home.html')

@main.route('/form')
def form():
    return render_template('form.html')

@main.route('/results', methods=['POST'])
def results():
    car_type = request.form.get('car_type')
    budget = request.form.get('budget')
    features = request.form.get('features')
    print(car_type)
    
    # Filter by active cars only
    cars = Car.query.filter_by(make=car_type, is_active=True).distinct(Car.model, Car.year).all()
    print(len(cars))
    return render_template('results.html', cars=cars)

@main.route('/car/<int:car_id>')
def car_detail(car_id):
    # Filter by active cars only
    car = Car.query.filter_by(id=car_id, is_active=True).first_or_404()
    return render_template('detail.html', car=car)

# Route to fetch car data as JSON
@main.route('/cars', methods=['GET'])
def get_cars():
    cars = Car.query.filter_by(is_active=True).all()
    cars_list = [
        {
            "id": car.id,
            "make": car.make,
            "model": car.model,
            "year": car.year,
            "fuel_type": car.fuel_type,
            "drive": car.drive,
            "cylinders": car.cylinders,
            "transmission": car.transmission,
            "city_mpg": car.city_mpg,
            "highway_mpg": car.highway_mpg,
            "combined_mpg": car.combined_mpg,
            "price": car.price
        } for car in cars
    ]
    return jsonify(cars_list)

# New route to add a car
@main.route('/add_car', methods=['GET', 'POST'])
def add_car():
    if request.method == 'POST':
        # Get data from the form
        make = request.form['make']
        model = request.form['model']
        year = request.form['year']
        fuel_type = request.form['fuel_type']
        drive = request.form['drive']
        cylinders = request.form['cylinders']
        transmission = request.form['transmission']
        city_mpg = request.form['city_mpg']
        highway_mpg = request.form['highway_mpg']
        combined_mpg = request.form['combined_mpg']
        price = request.form['price']

        # Create a new car record
        new_car = Car(
            make=make,
            model=model,
            year=year,
            fuel_type=fuel_type,
            drive=drive,
            cylinders=cylinders,
            transmission=transmission,
            city_mpg=city_mpg,
            highway_mpg=highway_mpg,
            combined_mpg=combined_mpg,
            price=price
        )

        # Add to the database
        db.session.add(new_car)

        # Commit to the database with error handling
        try:
            db.session.commit()
            flash('New car added successfully!', 'success')
        except Exception as e:
            db.session.rollback()  # Rollback the transaction in case of error
            print(f"Error occurred: {e}")
            flash('An error occurred while adding the car. Please try again.', 'danger')

        return redirect(url_for('main.home'))

    return render_template('new_car.html')

# New route to update car status (On Sale and Available)
@main.route('/update_car_status/<int:car_id>', methods=['POST'])
def update_car_status(car_id):
    car = Car.query.get_or_404(car_id)
    
    # Update the on_sale and available fields
    car.on_sale = 'on_sale' in request.form
    car.available = 'available' in request.form
    
    # Commit to the database with error handling
    try:
        db.session.commit()
        flash('Car status updated successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        print(f"Error occurred: {e}")
        flash('An error occurred while updating the car status. Please try again.', 'danger')
    
    return redirect(url_for('main.car_detail', car_id=car_id))

# New route to soft delete (archive) a car
@main.route('/delete_car/<int:car_id>', methods=['POST'])
def delete_car(car_id):
    car = Car.query.get_or_404(car_id)
    car.is_active = False  # Soft delete by setting is_active to False
    
    try:
        db.session.commit()
        flash('Car archived successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        print(f"Error occurred: {e}")
        flash('An error occurred while archiving the car. Please try again.', 'danger')
    
    return redirect(url_for('main.home'))

# Route to view archived cars
@main.route('/archive')
def view_archive():
    archived_cars = Car.query.filter_by(is_active=False).all()
    return render_template('archive.html', cars=archived_cars)

# Route to restore an archived car
@main.route('/restore_car/<int:car_id>', methods=['POST'])
def restore_car(car_id):
    car = Car.query.get_or_404(car_id)
    car.is_active = True  # Restore car by setting is_active to True
    
    try:
        db.session.commit()
        flash('Car restored successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        print(f"Error occurred: {e}")
        flash('An error occurred while restoring the car. Please try again.', 'danger')
    
    return redirect(url_for('main.view_archive'))
