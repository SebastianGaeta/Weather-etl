import requests
import csv
import logging

base_url = f"https://api.weather.gov" # global
headers = { # user agent
    "User-Agent": "https://github.com/SebastianGaeta" 
}
timeout = 10 # timeout
city_coordinates = { # cities 
    "New York City": ("40.714", "-74.006"),
    "Los Angeles": ("34.052", "-118.244"),
    "Chicago": ("41.878", "-87.629"),
    "Houston": ("29.760", "-95.369"),
    "Phoenix": ("33.448", "-112.074"),
    "Philadelphia": ("39.952", "-75.165"),
    "San Antonio": ("29.424", "-98.494"),
    "San Diego": ("32.715", "-117.161"),
    "Dallas": ("32.776", "-96.797"),
    "San Jose": ("37.338", "-121.886"),
    "Austin": ("30.267", "-97.743"),
    "Jacksonville": ("30.332", "-81.655"),
    "San Francisco": ("37.774", "-122.419"),
    "Columbus": ("39.961", "-82.999"),
    "Fort Worth": ("32.755", "-97.330"),
    "Indianapolis": ("39.768", "-86.158"),
    "Charlotte": ("35.227", "-80.843"),
    "Seattle": ("47.606", "-122.332"),
    "Denver": ("39.739", "-104.990"),
    "Washington D.C.": ("38.907", "-77.037"),
    "Boston": ("42.360", "-71.058"),
    "El Paso": ("31.761", "-106.485"),
    "Nashville": ("36.162", "-86.781"),
    "Detroit": ("42.331", "-83.045"),
    "Oklahoma City": ("35.468", "-97.516"),
    "Portland": ("45.505", "-122.675"),
    "Las Vegas": ("36.169", "-115.139"),
    "Memphis": ("35.149", "-90.049"),
    "Louisville": ("38.253", "-85.759"),
    "Baltimore": ("39.290", "-76.612"),
    "Milwaukee": ("43.038", "-87.907"),
    "Albuquerque": ("35.085", "-106.650"),
    "Tucson": ("32.222", "-110.974"),
    "Fresno": ("36.737", "-119.787"),
    "Sacramento": ("38.581", "-121.494"),
    "Kansas City": ("39.099", "-94.578"),
    "Mesa": ("33.415", "-111.831"),
    "Atlanta": ("33.749", "-84.388"),
    "Miami": ("25.761", "-80.191"),
    "Cleveland": ("41.499", "-81.694"),
    "Minneapolis": ("45.000", "-93.000"),
    "St. Louis": ("38.627", "-90.199"),
    "Pittsburgh": ("40.440", "-79.995"),
    "Orlando": ("28.538", "-81.379"),
    "New Orleans": ("29.951", "-90.071"),
    "Salt Lake City": ("40.760", "-111.891"),
    "Honolulu": ("21.309", "-157.858"),
    "Anchorage": ("61.218", "-149.900")
}
logging.basicConfig(filename="run.log", level="INFO") # config logging


def get_gridCordinates(lat: str, lon: str):
    """Return gridX, gridY, and gridId for a given latitute and longitude. On failure, prints status code and return None"""
    url = f"{base_url}/points/{lat},{lon}"
    response = requests.get(url, headers=headers, timeout=timeout)
    if (response.ok):
        response = response.json()
        return str(response["properties"]["gridX"]), str(response["properties"]["gridY"]), str(response["properties"]["gridId"])
    else:
        logging.error(f"Request failed with status code: {response.status_code}")
    return None

# returns office id, gridx, and gridy for given latitute and longitude
def get_data(city: str, office_id: str, gridX: str, gridY) -> list: 
    """Return data consisting of windSpeed, WindDirection, temperature, and corresponding time of measurement. On failure,
    print status code and return None"""
    url = f"{base_url}/gridpoints/{office_id}/{gridX},{gridY}/forecast"
    
    response = requests.get(url, headers=headers, timeout=timeout)
    if (response.ok):
        response = response.json()
        data = [city,
                response["properties"]["periods"][0]["windSpeed"],
                response["properties"]["periods"][0]["windDirection"],
                response["properties"]["periods"][0]["temperature"],
                response["properties"]["generatedAt"]]
        return data
    else:
        logging.error(f"Request failed with status code: {response.status_code}")
    return None 


data = []
for city in city_coordinates:
    lat = city_coordinates[city][0]
    lon = city_coordinates[city][1]
    try:
        gridX, gridY, gridId = get_gridCordinates(lat = lat, lon = lon)
        city_data = get_data(city, office_id=gridId, gridX=gridX, gridY=gridY)
        data.append(city_data)
        logging.info(f"Logged data for: {city}")

    except Exception as e: 
        logging.warning(f"Failed to log data for {city}: {e}")

with open("data.csv", "w", newline="") as fp:
    writer = csv.writer(fp)
    writer.writerow(["city","windSpeed","windDirection","temperature","date"]) # file header
    writer.writerows(data)

logging.info("   ***Session complete***   ")