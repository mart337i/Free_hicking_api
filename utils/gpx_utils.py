from ast import Pass
import math
import gpxpy
import gpxpy.gpx
from models.trail import Trail
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

DEBUG : bool = bool(os.getenv("DEBUGMODE"))
GPX_XSD_PATH = str(os.getenv("GPX_XSD_PATH"))
GPX_STORAGE_PATH = str(os.getenv("GPX_STORAGE_PATH"))




def validate_gpx_file(filename : str) -> bool: 
    if not filename.endswith(".gpx"):
        return False
    
    return True

def calculate_total_distance(coords):
    def haversine(coord1, coord2):
        lat1, lon1 = coord1
        lat2, lon2 = coord2
        R = 6371  # Earth radius in kilometers

        dLat = math.radians(lat2 - lat1)
        dLon = math.radians(lon2 - lon1)
        a = math.sin(dLat/2) * math.sin(dLat/2) + math.cos(math.radians(lat1)) \
            * math.cos(math.radians(lat2)) * math.sin(dLon/2) * math.sin(dLon/2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        return R * c

    total_distance = 0
    for i in range(1, len(coords)):
        # Extracting latitude and longitude from GPXTrackPoint objects
        lat1, lon1 = coords[i - 1].latitude, coords[i - 1].longitude
        lat2, lon2 = coords[i].latitude, coords[i].longitude

        total_distance += haversine((lat1, lon1), (lat2, lon2))

    return total_distance


def estimate_walking_time(distance_km):
    average_speed_kmh = 5  # Average walking speed in km/h
    time_hours = distance_km / average_speed_kmh
    hours = int(time_hours)
    minutes = int((time_hours - hours) * 60)

    return hours, minutes

def estimate_walking_float(distance_km):
    average_speed_kmh = 5  # Average walking speed in km/h

    # Time in hours (as a float)
    time_hours = distance_km / average_speed_kmh

    return time_hours


def get_gpx_info(filename : str):
    
    
    file_path = os.path.join(GPX_STORAGE_PATH, filename)

    # Check if the file exists
    if not os.path.isfile(file_path):
        return {
            "name" : "",
            "points" : [],
            "file_path" : ""
        }
    
    gpx_file = open(file_path, 'r')
    gpx = gpxpy.parse(gpx_file)

    points = []
    name = ""


    for track in gpx.tracks:
        name = track.name
        for segment in track.segments:
            for point in segment.points:
                points.append(point)
    
    return {
        "name" : name,
        "points" : points,
        "file_path" : file_path
    }

