import requests

GOOGLE_API_KEY = 'AIzaSyBMTwxml0qqFhVy6NrkBg8gyvd_mAk1Drc'

import requests

def fetch_route_traffic_data(start_coords, end_coords):
    """
    Fetch traffic data between two coordinates using Google Maps Directions API.

    Args:
        start_coords (dict): A dictionary containing "lat" and "lng" for the starting point.
        end_coords (dict): A dictionary containing "lat" and "lng" for the ending point.

    Returns:
        dict: A dictionary containing "distance" (in km) and "time" (in seconds).
    """
    api_key = GOOGLE_API_KEY
    url = (
        f"https://maps.googleapis.com/maps/api/directions/json?"
        f"origin={start_coords['lat']},{start_coords['lng']}&"
        f"destination={end_coords['lat']},{end_coords['lng']}&"
        f"key={api_key}"
    )

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if data["status"] == "OK":
            route = data["routes"][0]["legs"][0]
            distance = route["distance"]["value"] / 1000.0  # Convert meters to kilometers
            duration = route["duration"]["value"]  # Time in seconds

            return {"distance": distance, "time": duration}
        else:
            raise ValueError(f"API error: {data['status']} - {data.get('error_message', '')}")
    except Exception as e:
        print(f"Error fetching route traffic data: {e}")
        return {"distance": 0, "time": 0}

def calculate_fuel_cost(distance, mileage, fuel_price):
    """
    Calculate fuel cost for a given distance, mileage, and fuel price.

    Args:
        distance (float): Distance traveled in kilometers.
        mileage (float): Vehicle mileage in kilometers per liter.
        fuel_price (float): Price of fuel per liter in PKR.

    Returns:
        float: Total fuel cost in PKR.
    """
    if mileage <= 0:
        raise ValueError("Mileage must be greater than 0")
    liters_used = distance / mileage
    return round(liters_used * fuel_price, 2)


from datetime import time

def seconds_to_time(seconds):
    # Calculate hours, minutes, and remaining seconds
    hours = seconds // 3600  # Number of full hours
    minutes = (seconds % 3600) // 60  # Remaining minutes after hours
    remaining_seconds = seconds % 60  # Remaining seconds after minutes

    # Ensure the hours, minutes, and seconds are in two digits
    return time(hours, minutes, remaining_seconds, 0)

from datetime import datetime, timedelta

def time_to_seconds(time_obj):
    # Extract hours, minutes, and seconds from the time object
    hours = time_obj.hour
    minutes = time_obj.minute
    seconds = time_obj.second

    # Convert time to total seconds
    total_seconds = hours * 3600 + minutes * 60 + seconds
    return total_seconds


from math import radians, cos, sin, sqrt, atan2
from transport.models import BusStop

from geopy.distance import geodesic

def find_closest_start_stop(current_location, stops):
    """
    Finds the closest start stop based on Haversine distance.
    :param current_location: (lat, lng) tuple for the current location.
    :param stops: List of (stop_id, lat, lng) tuples.
    :return: stop_id of the closest start stop.
    """
    if not stops:
        return None  # No stops available

    closest_stop = min(
        stops,
        key=lambda stop: geodesic((current_location[0], current_location[1]), (stop[1], stop[2])).meters
    )
    
    return closest_stop[0]  # Return the stop ID

