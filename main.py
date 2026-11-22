import os
from datetime import date, datetime, timedelta
import pandas as pd

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

#loop through a month and select 7 days at a time to join together.
start_date = date(2026, 11, 1)
end_date = date(2026, 11, 30)

all_asteroids = []
week = start_date

while week <= end_date:
    week_end = min(week + timedelta(days=6), end_date)

    print(f"Fetching data from {week} to {week_end}")
    data = fetch_week(start_date=week, end_date=week_end)

    asteroids_data = extract_asteroids(data)

    all_asteroids.extend(asteroids_data)

    week = week_end + timedelta(days=1)

save_csv(all_asteroids, "asteroids_data.csv")
