import mysql.connector
import logging

logging.basicConfig(filename="database.log", )

"""

"""

mydb = mysql.connector.connect(
    host="YOUR_HOST",
    user="YOUR_USERNAME",
    password="YOUR_PASSWORD",
    database="YOUR_DATABASE"
)


mycursor = mydb.cursor()

try:
    mycursor.execute("CREATE TABLE City_weather_data (city VARCHAR(50), windSpeed int UNSIGNED, windDirection VARCHAR(50), temperature smallint, date VARCHAR(50), CONSTRAINT UC_weather UNIQUE (city,date))")
    logging.info("Successfully created table")
except Exception as e:
    logging.warning(f"{e}")
    




