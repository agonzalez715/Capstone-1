import requests
import time
from models import Car, db

API_URL = 'https://api.api-ninjas.com/v1/cars'
API_KEY = 'x7x0D1sdN22k7u8tRHmzOA==LgF0N2qcNQsHQyrM'

def fetch_car_data(make=None, model=None, fuel_type=None, drive=None, cylinders=None,
                   transmission=None, year=None, min_city_mpg=None, max_city_mpg=None,
                   min_hwy_mpg=None, max_hwy_mpg=None, min_comb_mpg=None, max_comb_mpg=None, 
                   limit=5):
    params = {
        'make': make,
        'model': model,
        'fuel_type': fuel_type,
        'drive': drive,
        'cylinders': cylinders,
        'transmission': transmission,
        'year': year,
        'min_city_mpg': min_city_mpg,
        'max_city_mpg': max_city_mpg,
        'min_hwy_mpg': min_hwy_mpg,
        'max_hwy_mpg': max_hwy_mpg,
        'min_comb_mpg': min_comb_mpg,
        'max_comb_mpg': max_comb_mpg,
        'limit': limit
    }

    # Remove any parameters that are None
    params = {k: v for k, v in params.items() if v is not None}

    headers = {
        'X-Api-Key': API_KEY
    }
    response = requests.get(API_URL, headers=headers, params=params)
    if response.status_code == 200:
        try:
            return response.json()
        except ValueError:
            print("Error: JSON response could not be decoded.")
            return None
    elif response.status_code == 429:
        print("Rate limit exceeded. Retrying...")
        time.sleep(5)  # Wait for 5 seconds before retrying
        return fetch_car_data(make, model, fuel_type, drive, cylinders, transmission, 
                              year, min_city_mpg, max_city_mpg, min_hwy_mpg, max_hwy_mpg, 
                              min_comb_mpg, max_comb_mpg, limit)
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

def seed_car_data():
    makes = ["Toyota", "Honda", "Ford"]  # Add more makes as needed
    for make in makes:
        params = {'make': make}
        car_data = fetch_car_data(**params)
        if car_data:
            for car in car_data:
                new_car = Car(
                    make=car.get('make', 'Unknown'),
                    model=car.get('model', 'Unknown'),
                    year=car.get('year', 0),
                    fuel_efficiency=car.get('fuel_efficiency', 'Unknown'),
                    safety_rating=car.get('safety_rating', 'Unknown'),
                    type=car.get('type', 'Unknown'),
                    features=car.get('features', '')
                )
                db.session.add(new_car)
    
    db.session.commit()
