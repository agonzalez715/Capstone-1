from app import create_app, db
from app.models import Car
from app.car_service import fetch_car_data

app = create_app()

with app.app_context():
    db.create_all()

    params = {
        'make': 'Toyota',  # Example parameter, adjust as needed
    }
    car_data = fetch_car_data(params)
    if car_data:
        for car in car_data:
            new_car = Car(
                make=car['make'],
                model=car['model'],
                year=car['year'],
                price=car['price'],
                fuel_efficiency=car.get('fuel_efficiency'),
                safety_rating=car.get('safety_rating')
            )
            db.session.add(new_car)
        db.session.commit()
        print("Database seeded with car data.")
    else:
        print("No data fetched from the API.")
