from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash
from models import Car, db

# Create a Blueprint named 'main' to organize your routes
main = Blueprint('main', __name__)

# Home route: Displays the homepage
@main.route('/')
def home():
    return render_template('home.html')

# Form route: Displays a form where users can search for cars
@main.route('/form')
def form():
    return render_template('form.html')

# Results route: Displays the search results based on user input from the form
@main.route('/results', methods=['POST'])
def results():
    car_type = request.form.get('car_type')
    budget = request.form.get('budget')
    features = request.form.get('features')
    print(car_type)
    
    # Query the database to filter cars by the selected make and ensure no duplicates by considering unique combinations of make, model, and year
    #.distinct(Car.make, Car.model, Car.year)
    print(len(cars))
    return render_template('results.html', cars=cars)

# Car details route: Displays the details of a specific car
@main.route('/car/<int:car_id>')
def car_detail(car_id):
    # Query the database to get the car by its ID and ensure it's active
    car = Car.query.filter_by(id=car_id, is_active=True).first_or_404()
    return render_template('detail.html', car=car)

# Route to fetch car data as JSON
@main.route('/cars', methods=['GET'])
def get_cars():
    # Query the database to get all active cars, ensuring no duplicates
    cars = db.session.query(Car).filter_by(is_active=True).distinct(Car.make, Car.model, Car.year).all()
    # Prepare the data in JSON format
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

# Route to add a new car
@main.route('/add_car', methods=['GET', 'POST'])
def add_car():
    if request.method == 'POST':
        # Collect data from the form
        make = request.form['make'].strip()
        model = request.form['model'].strip()
        year = request.form['year'].strip()
        fuel_type = request.form['fuel_type'].strip()
        drive = request.form['drive'].strip()
        cylinders = request.form['cylinders'].strip()
        transmission = request.form['transmission'].strip()
        city_mpg = request.form['city_mpg'].strip()
        highway_mpg = request.form['highway_mpg']
        combined_mpg = request.form['combined_mpg'].strip()
        price = request.form['price'].strip()

        # Create a new Car object
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

        # Add the new car to the session and commit it to the database
        db.session.add(new_car)
        try:
            db.session.commit()  # Save the new car to the database
            flash('New car added successfully!', 'success')  # Display a success message
        except Exception as e:
            db.session.rollback()  # Rollback the transaction in case of error
            print(f"Error occurred: {e}")
            flash('An error occurred while adding the car. Please try again.', 'danger')

        return redirect(url_for('main.home'))

    return render_template('new_car.html')  # Display the form to add a new car

# Route to update car status (On Sale and Available)
@main.route('/update_car_status/<int:car_id>', methods=['POST'])
def update_car_status(car_id):
    car = Car.query.get_or_404(car_id)
    
    # Update the car's status based on form input
    car.on_sale = 'on_sale' in request.form
    car.available = 'available' in request.form
    
    try:
        db.session.commit()  # Save the updated car status to the database
        flash('Car status updated successfully!', 'success')
    except Exception as e:
        db.session.rollback()  # Rollback the transaction in case of error
        print(f"Error occurred: {e}")
        flash('An error occurred while updating the car status. Please try again.', 'danger')
    
    return redirect(url_for('main.car_detail', car_id=car_id))

# Route to view all available cars (without duplicates)
@main.route('/show_all_cars', methods=['GET'])
def show_all_cars():
    # Query the database to get all active cars, ensuring no duplicates
    cars = db.session.query(Car).filter_by(is_active=True).distinct(Car.make, Car.model, Car.year).all()
    return render_template('results.html', cars=cars)  # Display the results

# Route to view archived cars
@main.route('/archive', methods=['GET'])
def view_archive():
    # Query the database to get all archived cars, ensuring no duplicates
    archived_cars = db.session.query(Car).filter_by(is_active=False).distinct(Car.make, Car.model, Car.year).all()
    return render_template('archive.html', cars=archived_cars)  # Display the archived cars

# Route to restore an archived car
@main.route('/restore_car/<int:car_id>', methods=['POST'])
def restore_car(car_id):
    car = Car.query.get_or_404(car_id)
    car.is_active = True  # Restore the car by setting is_active to True
    
    try:
        db.session.commit()  # Save the restored car to the database
        flash('Car restored successfully!', 'success')
    except Exception as e:
        db.session.rollback()  # Rollback the transaction in case of error
        print(f"Error occurred: {e}")
        flash('An error occurred while restoring the car. Please try again.', 'danger')

    return redirect(url_for('main.view_archive'))

# Route to archive (soft delete) a car
@main.route('/archive_car/<int:car_id>', methods=['POST'])
def archive_car(car_id):
    car = Car.query.get_or_404(car_id)
    car.is_active = False  # Soft delete the car by setting is_active to False
    
    try:
        db.session.commit()  # Save the archived car to the database
        flash('Car archived successfully!', 'success')
    except Exception as e:
        db.session.rollback()  # Rollback the transaction in case of error
        print(f"Error occurred: {e}")
        flash('An error occurred while archiving the car. Please try again.', 'danger')

    return redirect(url_for('main.home'))  # Redirect to the home page
