# AquaFusion - BSIT 4A - CPSTONE
import Adafruit_DHT
import time
import pyrebase
from config import config

DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 17

firebase = pyrebase.initialize_app(config)
db = firebase.database()

while True:
    humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
    if humidity is not None and temperature is not None:
        print("Temp={0:0.1f}C  Humidity={1:0.1f}%".format(temperature, humidity))

        if temperature < 35:
            message = "Ambient Temperature"
        elif temperature <= 40:
            message = "Warning Exceeding Ambient Temperature"
        elif temperature <= 50:
            message = "Exceeding Maximum Temperature"
        else:
            message = "Temperature within a safe range"

        print(message)

        # Create a dictionary with the data you want to send to Firebase
        data = {
            "temperature": temperature,
            "humidity": humidity,
            "status": message
        }

        # Send the data to Firebase Realtime Database
        db.child("DHT22_temphum").set(data)

    else:
        print("Sensor failure. Check wiring.")

    time.sleep(3)  # Adjust the sleep interval for DHT22 readings