# NOAA Weather ETL 

### Overview
This project is a simple **Extract-Transform-Load (ETL)** pipeline built in Python that collects real-time weather forecast data for multiple U.S. cities from the [National Weather Service (NOAA) API](https://api.weather.gov/).  
It extracts forecast data, cleans and transforms it, then loads it into a **MySQL database** for long-term storage and analysis.

---
```
## Project Structure

weather_etl/
│
├── extract_weather.py      # Extracts data from NOAA API → data.csv
├── load_to_mysql.py        # Reads data.csv, transforms & loads to MySQL
├── create_table.py         # Creates database table with unique constraint
├── data.csv                # Output file (auto-generated)
├── run.log                 # Log file (auto-generated)
└── README.md               # Project documentation
```
---

## How It Works

### **1. Extract**
- Uses the NOAA API endpoint `/points/{lat},{lon}` to retrieve grid coordinates for each city.
- Calls `/gridpoints/{officeId}/{gridX},{gridY}/forecast` to get the latest forecast data.
- Extracts:  
  - `windSpeed`  
  - `windDirection`  
  - `temperature`  
  - `generatedAt` (timestamp)
- Saves all data into `data.csv` along with city names.

### **2. Transform**
- Cleans the CSV data by:
  - Parsing numeric wind speeds (handles values like “0 to 10 mph”).
  - Converting temperature to integers.
  - Formatting timestamps into `VARCHAR()`.
- Ensures clean, structured records ready for database insertion.

### **3. Load**
- Inserts data into a MySQL table called `City_weather_data`.
- Enforces a **unique constraint on `(city, date)`** to prevent duplicate records.
- Logs successful inserts and skipped duplicates.

---

## Example MySQL Schema
```sql
CREATE TABLE City_weather_data (
    city VARCHAR(50),
    windSpeed INT UNSIGNED,
    windDirection VARCHAR(50),
    temperature SMALLINT,
    date VARCHAR(50),
    CONSTRAINT UC_weather UNIQUE (city, date)

);
