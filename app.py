import os
from flask import Flask, render_template, request
import requests
from dotenv import load_dotenv

# TODO
# - Get Ticketmaster API to work... done!
# - Get Amadeus Hotel API to work
# - Fix CSS to make it look pretty!

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Ticketmaster API
TICKETMASTER_API_KEY = "fuDhyQsrlyPj2c8vFLOtKZsKfApDkpQj"  # API Key
BASE_URL_TICKETMASTER = "https://app.ticketmaster.com/discovery/v2/events.json"

# Amadeus API
# AMADEUS_API_KEY = "DK7DT275X0EiBEe8RMFX6rilIKRihrvO"  # API key
# BASE_URL_AMADEUS_AUTH = "https://test.api.amadeus.com/v1/security/oauth2/token"
# BASE_URL_AMADEUS_HOTELS = "https://test.api.amadeus.com/v2/shopping/hotel-offers"


# Function to authenticate with the Amadeus API
# def get_amadeus_token():
#     payload = {
#         "grant_type": "client_credentials",
#         "client_id": AMADEUS_API_KEY,
#         "client_secret": AMADEUS_API_SECRET,
#     }
#     response = requests.post(BASE_URL_AMADEUS_AUTH, data=payload)
#     if response.status_code == 200:
#         token = response.json()["access_token"]
#         print(f"Amadeus Token: {token}")  # Debugging line
#         return token
#     else:
#         print(f"Error authenticating with Amadeus API: {response.status_code}, {response.json()}")
#         return None


# # Function to get hotels in Seattle
# def get_seattle_hotels(start_date=None, end_date=None):
#     token = get_amadeus_token()
#     if not token:
#         return []
    
#     headers = {"Authorization": f"Bearer {token}"}
#     params = {
#     "cityCode": "SEA",  # Seattle's IATA code
#     "currency": "USD",  # Specify the currency (e.g., USD)
#     "checkInDate": f"{start_date}T00:00:00Z",  # Ensure valid dates
#     "checkOutDate":  f"{end_date}T23:59:59Z"
    
# }

#     response = requests.get(BASE_URL_AMADEUS_HOTELS, headers=headers, params=params)
    
#     if response.status_code == 200:
#         data = response.json()
#         return data["data"] if "data" in data else []
#     else:
#         print(f"Error fetching hotels: {response.status_code}, {response.json()}")
#         return []

# Function to get events in Seattle, with optional date filters
def get_seattle_attractions(start_date=None, end_date=None):
    params = {
        "city": "Seattle",  # Search for events in Seattle
        "checkInDate": start_date,
        "checkOutDate": end_date,
        "apikey": TICKETMASTER_API_KEY,  # API Key
    }
    response = requests.get(BASE_URL_TICKETMASTER, params=params)
    if response.status_code == 200:
        data = response.json()
        return data["_embedded"]["events"] if "_embedded" in data else []
    else:
        print(f"Error fetching events: {response.status_code}, {response.json()}")
        return []

# Flask route to show the home page (search form)
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        start_date = request.form['start_date']  # User input for start date
        end_date = request.form['end_date']  # User input for end date

        # Get events in Seattle for the specified date range
        events = get_seattle_attractions(start_date, end_date)

        # Get hotels in Seattle
       # hotels = get_seattle_hotels(start_date, end_date)


        # Pass both events and hotels to the results page
        return render_template('results.html', events=events)
    
    # Render the home page with the search form
    return render_template('index.html')

# Runs Flask app
if __name__ == "__main__":
    app.run(debug=True)
