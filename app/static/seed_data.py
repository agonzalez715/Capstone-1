from app import create_app  # Import the create_app function from the app module
from models import Car, db  # Import the Car model and db (SQLAlchemy) instance from the models module
from car_service import fetch_car_data  # Import the fetch_car_data function from the car_service module

app = create_app()  # Create an instance of the Flask app by calling the create_app function

# Use the app context to interact with the database
with app.app_context():  # Ensure that the application context is available when interacting with the database
    db.create_all()  # Create all tables in the database based on the models defined

    makes = ["Toyota", "Honda", "Ford"]  # Define a list of car manufacturers (makes) to fetch data for

    for make in makes:  # Loop over each car make in the makes list
        car_data = fetch_car_data(make=make)  # Fetch car data for the current make from the API using the fetch_car_data function
        if car_data:  # Check if any data was returned from the API
            for car in car_data:  # Loop through each car returned in the data
                # Create a new Car object using only the fields from the API and the Car model
                new_car = Car(
                    make=car.get('make', 'Unknown'),  # Set the 'make' field, default to 'Unknown' if not provided
                    model=car.get('model', 'Unknown'),  # Set the 'model' field, default to 'Unknown' if not provided
                    year=car.get('year', 0),  # Set the 'year' field, default to 0 if not provided
                    fuel_type=car.get('fuel_type', 'Unknown'),  # Set the 'fuel_type' field, default to 'Unknown' if not provided
                    drive=car.get('drive', 'Unknown'),  # Set the 'drive' field, default to 'Unknown' if not provided
                    cylinders=car.get('cylinders', 0),  # Set the 'cylinders' field, default to 0 if not provided
                    transmission=car.get('transmission', 'Unknown'),  # Set the 'transmission' field, default to 'Unknown' if not provided
                    city_mpg=car.get('city_mpg', 0),  # Set the 'city_mpg' field, default to 0 if not provided
                    highway_mpg=car.get('highway_mpg', 0),  # Set the 'highway_mpg' field, default to 0 if not provided
                    combined_mpg=car.get('combined_mpg', 0),  # Set the 'combined_mpg' field, default to 0 if not provided
                    price=car.get('price', 0.0)  # Set the 'price' field, default to 0.0 if not provided
                )
                db.session.add(new_car)  # Add the new car object to the current database session
            db.session.commit()  # Commit the session to save the new cars to the database
            print(f"Database seeded with {make} car data.")  # Print a confirmation message for each make
        else:
            print(f"No data fetched for {make} from the API.")  # Print a message if no data was fetched for the make
