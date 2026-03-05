import time
import pandas as pd
from datetime import datetime
try:
    from gpiozero import MotionSensor
except Exception:
    MotionSensor = None

# This script reads data from a PIR motion sensor connected to a Raspberry Pi, collects the data for a specified duration and interval, and exports it to an Excel file.
# Text that follows the '#' symbol is a comment and is not executed as part of the code. It provides explanations and instructions for the user.

# This code requires pandas to export to an Excel file, to install pandas, run: sudo apt install python3-pandas

# Wiring the Hardware
# Connect PIR motion sensor to Raspberry Pi GPIO pins as follows:
# VDC → 5V VDC (Pin 2)
# GND → GND (Pin 6)
# VCC → VCC (Pin 23)

# GPIO pin for the PIR motion sensor, change this if your sensor is connected to a different pin
PIN = 23

# Setup motion sensor
sensor = MotionSensor(PIN)

# Function to read PIR motion sensor data
def read_motion():
    return sensor.is_active

# Function to collect data for a specified duration and interval
def collect_data(duration_minutes, interval_seconds):
    data = []
    start_time = time.time()
    duration_seconds = duration_minutes * 60

    while time.time() - start_time < duration_seconds:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        motion = read_motion()
        data.append([timestamp, motion])
        print(f"Timestamp: {timestamp}, Motion Detected: {motion}")
        time.sleep(interval_seconds)

    return data

# Function to export data to Excel
def export_to_excel_file(data, filename):
    df = pd.DataFrame(data, columns=['Timestamp', 'Motion'])
    df.to_excel(filename, index=False)
    print(f"Data saved to {filename}")

# Example usage
if __name__ == "__main__":
    duration_minutes = 5  # Set the duration here in minutes
    interval_seconds = 10  # Set the interval here in seconds
    data = collect_data(duration_minutes, interval_seconds)
    export_to_excel_file(data, 'motion_data.xlsx')
