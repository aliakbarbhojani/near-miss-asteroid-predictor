import os

import requests
from dotenv import load_dotenv
import csv

# Takes in start and end date, returns a list of asteroids that will make a close approach to Earth.
def fetch_week(start_date, end_date):
    params = {
    "start_date": start_date,
    "end_date": end_date,
    "api_key": API_KEY,
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

# Extracts relevant asteroid data from the NASA API response.
def extract_asteroids(data):
    days = data["near_earth_objects"]

    asteroids_data = []

    for date in sorted(days):
        for asteroid in days[date]:

            asteroids_data.append({
                "date": date,
                "name": asteroid["name"],
                "hazardous": asteroid["is_potentially_hazardous_asteroid"],
                "size": asteroid["estimated_diameter"]["meters"]["estimated_diameter_max"],
                "velocity": float(asteroid["close_approach_data"][0]["relative_velocity"]["kilometers_per_hour"]),
                "miss_distance": float(asteroid["close_approach_data"][0]["miss_distance"]["kilometers"]),
            })

    return asteroids_data

# Saves the extracted asteroid data to a CSV file.
def save_csv(asteroids_data, filename):
    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["date", "name", "hazardous", "size", "velocity", "miss_distance"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for asteroid in asteroids_data:
            writer.writerow(asteroid)

# Read the .env file and pull the key out of it, so the key never lives in the code.
load_dotenv()
API_KEY = os.getenv("NASA_API_KEY")

# Set the base URL for the NASA NEO API.
url = "https://api.nasa.gov/neo/rest/v1/feed"

# Fetch the asteroid data for the specified week.
data = fetch_week(start_date="2026-11-01", end_date="2026-11-07")
print(data.keys())

# Extract the relevant asteroid data and save it to a CSV file.
asteroids_data = extract_asteroids(data)
save_csv(asteroids_data, "asteroids_data.csv")


