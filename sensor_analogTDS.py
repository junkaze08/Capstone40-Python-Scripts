import time
import pyrebase
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from config import config

# Define the Lettuce ranges
lettuce_cf_range = (8, 12)  # Conductivity Factor (cF)
lettuce_ec_range = (0.8, 1.2)  # Electro-Conductivity (EC) in mS
lettuce_ppm_range = (560, 840)  # PPM

# Initialize Firebase
firebase = pyrebase.initialize_app(config)
db = firebase.database()

# Initialize the I2C bus and ADS1115 ADC
i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c)

# Create an analog input channel on the ADS1115 (A0 in this example)
chan = AnalogIn(ads, ADS.P0)

print("Data sent to Firebase successfully")
while True:
    try:
        # Read TDS data from the analog sensor connected to the ADS1115
        tds_raw = chan.value  # Read the analog value directly
        print("TDS Raw Value:", tds_raw)

        # Convert TDS to EC, cF, and PPM using the provided conversion factors
        cf_value = tds_raw / 640.0
        ec_value = cf_value / 10.0
        ppm_value = ec_value * 700.0

        def check_ranges(value, value_range):
            # Check if a value is within the specified range
            return value_range[0] <= value <= value_range[1]

        in_cf_range = check_ranges(cf_value, lettuce_cf_range)
        in_ec_range = check_ranges(ec_value, lettuce_ec_range)
        in_ppm_range = check_ranges(ppm_value, lettuce_ppm_range)

        print("Electro-Conductivity (EC) in mS: {:.1f}".format(ec_value))
        print("Conductivity Factor (cF): {:.1f}".format(cf_value))
        print("Parts per million (PPM): {:.1f}".format(ppm_value))


        # Dictionary with the data to send to Firebase
        data = {
            "tds_raw": tds_raw,
            "ec_mS": ec_value,
            "cF": cf_value,
            "ppm": ppm_value,
            # Add more data as needed
        }

        # Send the data to Firebase Realtime Database
        db.child("TDS_data").set(data)
        
        time.sleep(3)

    except KeyboardInterrupt:
        break