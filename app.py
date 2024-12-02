import os
from flask import Flask, render_template, request, redirect, url_for
import requests
from dotenv import load_dotenv

#TODO 
# - get ticket master API to work... done!!!
# - get hotel api to work
# - fix CSS to make it look pretty!

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Get the API key from the environment variable
TICKETMASTER_API_KEY = "fuDhyQsrlyPj2c8vFLOtKZsKfApDkpQj" # os.getenv("TICKETMASTER_API_KEY")
BASE_URL_TICKETMASTER = "https://app.ticketmaster.com/discovery/v2/events.json"

# Function to get events in Seattle, with optional date filters
def get_seattle_attractions(start_date=None, end_date=None):
    params = {
    "city": "Seattle",  # Search for events in Seattle
    "startDateTime": f"{start_date}T00:00:00Z",
    "endDateTime": f"{end_date}T23:59:59Z",
    "apikey": TICKETMASTER_API_KEY,  # Ensures the API Key is included
}

    response = requests.get(BASE_URL_TICKETMASTER, params=params)
    print(f"API Key: {TICKETMASTER_API_KEY}")

    # Add date filters if provided
    if start_date:
        params["startDateTime"] = f"{start_date}T00:00:00Z"
    if end_date:
        params["endDateTime"] = f"{end_date}T23:59:59Z"
    
    # requests to the Ticketmaster API 
    response = requests.get(BASE_URL_TICKETMASTER, params=params)
    
    if response.status_code == 200:
        data = response.json()
        print(data)  # for debugging: See the API response for ME
        
        # Return events if available
        return data["_embedded"]["events"] if "_embedded" in data else []
    else:
        print(f"Error: {response.status_code}, {response.json()}")
        return []

# Flask route to show the home page (search form)
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        start_date = request.form['start_date']  # User input for start date
        end_date = request.form['end_date']  # User input for end date
        
        # Get events in Seattle for the specified date range
        events = get_seattle_attractions(start_date, end_date)

        # Debugging: Check the events  FOR ME
        print(events)  # This should print a list of events

        # Redirect to results page with events data
        return render_template('results.html', events=events)
    
    # Render the home page with the search form
    return render_template('index.html')

# Runs  Flask 
if __name__ == "__main__":
    app.run(debug=True)
