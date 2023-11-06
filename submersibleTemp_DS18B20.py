# AquaFusion - BSIT 4A - CPSTONE
import time
import pyrebase
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from config import config

# Initialize Firebase
firebase = pyrebase.initialize_app(config)
db = firebase.database()

# Initialize the I2C bus and ADS1115 ADC
i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c)

# Create an analog input channel on the ADS1115 (A0 in this example)
chan = AnalogIn(ads, ADS.P0)

def read_analog_temperature():
    try:
        # Read analog voltage from the ADS1115
        analog_value = chan.value
        voltage = analog_value * 0.0001875  # 3.3V reference voltage

        # Convert the voltage to temperature
        # Modify this part based on your specific temperature sensor
        temperature = voltage  # Modify this line for your temperature conversion

        return temperature
    except Exception as e:
        print(f"Error reading analog temperature: {e}")
        return None

while True:
    temperature = read_analog_temperature()

    if temperature is not None:
        print(f"Temperature: {temperature}°C")

        # Create a dictionary with the data to send to Firebase
        data = {"temperature": temperature}

        # Send the data to Firebase Realtime Database
        db.child("analog_temperature_data").set(data)
    else:
        print("Error reading temperature data")

    time.sleep(10)  # Adjust the sleep interval as needed