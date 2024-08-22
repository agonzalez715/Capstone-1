import requests
import time
from models import Car, db

# API endpoint and API key for accessing car data from the API
API_URL = 'https://api.api-ninjas.com/v1/cars'
API_KEY = 'x7x0D1sdN22k7u8tRHmzOA==LgF0N2qcNQsHQyrM'  # Replace with your actual API key

# Function to fetch car data from the API
def fetch_car_data(make=None, model=None, fuel_type=None, drive=None, cylinders=None,
                   transmission=None, year=None, min_city_mpg=None, max_city_mpg=None,
                   min_hwy_mpg=None, max_hwy_mpg=None, min_comb_mpg=None, max_comb_mpg=None, 
                   limit=5):
    # Parameters to be sent in the API request. Only include parameters that are not None.
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
        'limit': limit  # Limit the number of results returned by the API
    }

    # Remove any parameters that are None to clean up the request
    params = {k: v for k, v in params.items() if v is not None}

    # Headers for the API request, including the API key for authorization
    headers = {
        'X-Api-Key': API_KEY
    }
    
    # Make the GET request to the API with the specified parameters and headers
    response = requests.get(API_URL, headers=headers, params=params)
    
    # Check if the response is successful (status code 200)
    if response.status_code == 200:
        try:
            return response.json()  # Return the JSON data from the API response
        except ValueError:
            # Handle the case where the response cannot be decoded as JSON
            print("Error: JSON response could not be decoded.")
            return None
    elif response.status_code == 429:
        # Handle the case where the API rate limit is exceeded
        print("Rate limit exceeded. Retrying...")
        time.sleep(5)  # Wait for 5 seconds before retrying the request
        # Recursively call the function again with the same parameters
        return fetch_car_data(make, model, fuel_type, drive, cylinders, transmission, 
                              year, min_city_mpg, max_city_mpg, min_hwy_mpg, max_hwy_mpg, 
                              min_comb_mpg, max_comb_mpg, limit)
    else:
        # Handle other HTTP errors
        print(f"Error: {response.status_code} - {response.text}")
        return None

# Function to seed car data into the database
def seed_car_data():
    # List of car makes to fetch data for. You can add more makes as needed.
    makes = ["Toyota", "Honda", "Ford"]
    
    # Iterate over each make and fetch data for it
    for make in makes:
        params = {'make': make}  # Prepare the parameters for the API request
        car_data = fetch_car_data(**params)  # Fetch car data using the API
        
        # If data was successfully fetched, add it to the database
        if car_data:
            for car in car_data:
                # Create a new Car object using the data returned from the API
                new_car = Car(
                    make=car.get('make', 'Unknown'),  # Default to 'Unknown' if the field is missing
                    model=car.get('model', 'Unknown'),
                    year=car.get('year', 0),
                    fuel_efficiency=car.get('fuel_efficiency', 'Unknown'),  # Note: Align with the actual model fields
                    safety_rating=car.get('safety_rating', 'Unknown'),
                    type=car.get('type', 'Unknown'),
                    features=car.get('features', '')
                )
                # Add the new car record to the database session
                db.session.add(new_car)
    
    # Commit all the added records to the database
    db.session.commit()
