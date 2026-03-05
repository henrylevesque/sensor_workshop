import time
from datetime import datetime

# TEMPLATE FILE: Light Sensor Test
# This is a template for reading a simple digital or analog light sensor.
# Modify this based on your specific sensor type.

# Sensor Type: Photocell (light-dependent resistor) or digital light sensor
# Wiring: Depends on sensor (check your specific module's pinout)
# - If using ADS1115 ADC: Connect to A0-A3 pins (similar to sound_test.py)
# - If using GPIO: Connect to a GPIO pin and read digital HIGH/LOW

# Example: Using GPIO for a simple digital light sensor
from gpiozero import MotionSensor  # or InputDevice for digital input

# Replace PIN with the GPIO number where your light sensor is connected
PIN = 17  # Change this to match your wiring

try:
    light_sensor = InputDevice(PIN)
except ImportError:
    from gpiozero import InputDevice
    light_sensor = InputDevice(PIN)

print("=" * 70)
print("LIGHT SENSOR TEST")
print("=" * 70)
print("Reading light sensor every 2 seconds...")
print("Press Ctrl+C to stop.\n")

reading_count = 0

try:
    while True:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        light_level = light_sensor.value  # 1 = bright, 0 = dark (for digital sensor)
        
        reading_count += 1
        print(f"[{reading_count}] {timestamp} | Light Level: {light_level}")
        
        time.sleep(2)

except KeyboardInterrupt:
    print("\n" + "=" * 70)
    print(f"Test stopped. {reading_count} readings.")
    print("=" * 70)

# TIPS FOR STUDENTS:
# - If your sensor is analog, use the ADS1115 ADC (like sound_test.py)
# - If your sensor is digital, use InputDevice and GPIO pin
# - Check your sensor's data sheet for proper wiring and pin selection
# - Test with this file first before creating a data_logger version
