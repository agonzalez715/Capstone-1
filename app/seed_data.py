from app import create_app
from models import Car, db
from car_service import fetch_car_data

app = create_app()

with app.app_context():
    db.create_all()

    makes = ["Toyota", "Honda", "Ford"]  # Add more makes as needed

    for make in makes:
        car_data = fetch_car_data(make=make)
        if car_data:
            for car in car_data:
                # Create a new Car object using only the fields from the API and the Car model
                new_car = Car(
                    make=car.get('make', 'Unknown'),
                    model=car.get('model', 'Unknown'),
                    year=car.get('year', 0),
                    fuel_type=car.get('fuel_type', 'Unknown'),
                    drive=car.get('drive', 'Unknown'),
                    cylinders=car.get('cylinders', 0),
                    transmission=car.get('transmission', 'Unknown'),
                    city_mpg=car.get('city_mpg', 0),  # Assuming we get one value for city_mpg
                    highway_mpg=car.get('highway_mpg', 0),  # Assuming we get one value for highway_mpg
                    combined_mpg=car.get('combined_mpg', 0),  # Assuming we get one value for combined_mpg
                    price=car.get('price', 0.0)  # Assuming price if it's included
                )
                db.session.add(new_car)
            db.session.commit()
            print(f"Database seeded with {make} car data.")
        else:
            print(f"No data fetched for {make} from the API.")
