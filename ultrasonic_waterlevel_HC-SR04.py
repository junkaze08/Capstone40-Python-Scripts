# AquaFusion - BSIT 4A - CPSTONE
import RPi.GPIO as GPIO
import time
import pyrebase
from config import config

# Define GPIO pins for HC-SR04
TRIG = 23
ECHO = 24

firebase = pyrebase.initialize_app(config)
db = firebase.database()

try:
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)

    while True:
        GPIO.output(TRIG, False)
        time.sleep(2)

        GPIO.output(TRIG, True)
        time.sleep(0.00001)
        GPIO.output(TRIG, False)

        while GPIO.input(ECHO) == 0:
            pulse_start = time.time()

        while GPIO.input(ECHO) == 1:
            pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17150
        distance = round(distance, 2)

        print("Distance:", distance, "cm")

        # Create a dictionary with the data you want to send to Firebase
        data = {
            "distance": distance
        }

        # Send the data to Firebase Realtime Database
        db.child("ultrasonic_data_water").set(data)

except KeyboardInterrupt:
    print("Measurement stopped by the user.")

finally:
    GPIO.cleanup()

    time.sleep(2)  # Adjust the sleep interval for Ultrasonic sensor readings