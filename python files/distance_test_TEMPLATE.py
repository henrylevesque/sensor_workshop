import time
from datetime import datetime

# TEMPLATE FILE: Ultrasonic Distance Sensor Test
# This is a template for reading distance using an ultrasonic sensor.
# Popular model: HC-SR04

# Sensor Type: HC-SR04 Ultrasonic Distance Sensor
# Wiring:
# - VCC (5V) → 5V (Physical Pin 2)
# - GND → GND (Physical Pin 6)
# - TRIG → GPIO 17 (Physical Pin 11)
# - ECHO → GPIO 27 (Physical Pin 13)

import board
from gpiozero import DistanceSensor

# Create distance sensor (adjust GPIO pins if different)
sensor = DistanceSensor(echo=27, trigger=17)

print("=" * 70)
print("ULTRASONIC DISTANCE SENSOR TEST")
print("=" * 70)
print("Reading distance every 2 seconds...")
print("Press Ctrl+C to stop.\n")

reading_count = 0

try:
    while True:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        distance = sensor.distance * 100  # Convert to centimeters
        
        reading_count += 1
        print(f"[{reading_count}] {timestamp} | Distance: {distance:.1f} cm")
        
        time.sleep(2)

except KeyboardInterrupt:
    print("\n" + "=" * 70)
    print(f"Test stopped. {reading_count} readings.")
    print("=" * 70)

# TIPS FOR STUDENTS:
# - HC-SR04 typically measures 2cm to 4m distance
# - sensor.distance returns value in meters (multiply by 100 for cm)
# - Works best on hard, reflective surfaces
# - Adjust GPIO pins (17, 27) if wired to different pins
