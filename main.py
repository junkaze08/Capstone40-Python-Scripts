# AquaFusion - BSIT 4A - CPSTONE
import subprocess
import signal
import time

y = 0.1

python3_path = '/usr/bin/python3'

process1 = subprocess.Popen([python3_path, 'ultrasonic_plant_HC-SR04.py'])

time.sleep(y)

process2 = subprocess.Popen([python3_path, 'ultrasonic_waterlevel_HC-SR04.py'])

time.sleep(y)

process3 = subprocess.Popen([python3_path, 'submersibleTemp_DS18B20.py'])

time.sleep(y)

process4 = subprocess.Popen([python3_path, 'sensor_DHT22.py'])

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Ctrl+C detected. Stopping processes...")
    process1.send_signal(signal.SIGINT)
    process2.send_signal(signal.SIGINT)