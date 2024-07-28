import requests

API_URL = 'https://api.api-ninjas.com/v1/cars'
API_KEY = 'x7x0D1sdN22k7u8tRHmzOA==LgF0N2qcNQsHQyrM'  # Replace with your actual API key

def fetch_car_data(params):
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
        return fetch_car_data(params)
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None
