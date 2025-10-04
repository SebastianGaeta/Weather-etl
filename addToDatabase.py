from datetime import datetime
import mysql.connector
import logging

logging.basicConfig(filename="database.log")

mydb = mysql.connector.connect(
    host="YOUR_HOST",
    user="YOUR_USERNAME",
    password="YOUR_PASSWORD",
    database="YOUR_DATABASE"
)

mycursor = mydb.cursor()

data = []

with open("data.csv", "r") as csv_file:
    csv_file.readline() # skip first line

    for line in csv_file:
        parts = line.strip().split(",")
        city = parts[0]    
        windDirection = parts[2]
        temperature = int(parts[3]) 

        # Parse windSpeed
        windSpeed_parse = parts[1].split(" ")
        windSpeed_values = []
        for element in windSpeed_parse:
            if (element.isdigit()):
                windSpeed_values.append(int(element))
        windSpeed = max(windSpeed_values) 

        # format date
        dt_obj = datetime.fromisoformat(parts[4])
        date = dt_obj.strftime("%B %d, %Y")

        parts = (city, windSpeed, windDirection, temperature, date)
        data.append(parts)

try:
    sql = "INSERT INTO City_weather_data (city, windSpeed, windDirection, temperature, date) VALUES (%s, %s, %s, %s, %s)"
    for piece in data:
        try:
            mycursor.execute(sql, piece)
            logging.info(f"logged data: {piece}")
        except Exception as e:
            logging.error(f"{e}")
    mydb.commit()
except Exception as e:
    logging.error(f"{e}")



mycursor.execute("SELECT * FROM City_weather_data")
myresult = mycursor.fetchall()

for x in myresult:
    print(x)
