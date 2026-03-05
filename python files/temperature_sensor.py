import time
import pandas as pd
from datetime import datetime
try:
    import Adafruit_DHT
except Exception:
    Adafruit_DHT = None

# This script reads data from a DHT11 temperature sensor connected to a Raspberry Pi, collects the data for a specified duration and interval, and exports it to an Excel file.
# Text that follows the '#' symbol is a comment and is not executed as part of the code. It provides explanations and instructions for the user.

# This code requires pandas to export to an Excel file, to install pandas, run: sudo apt install python3-pandas
# This code requires the Adafruit DHT library, to install it, run: pip3 install Adafruit-DHT

# Wiring the Hardware
# Connect DHT11 temperature sensor to Raspberry Pi GPIO pins as follows:
# S → VCC (Pin 4)
# V → 5V VDC (Pin 2)
# G → GND (Pin 6)


# Sensor type and GPIO pin
SENSOR = Adafruit_DHT.DHT11
PIN = 4

# Function to read temperatureyusing pip3 install Adafruit-DHT data
def read_temperature():
    if Adafruit_DHT is None:
        raise RuntimeError("Adafruit_DHT library not available. Install Adafruit-DHT using pip3 install Adafruit-DHT")

    humidity, temperature = Adafruit_DHT.read_retry(SENSOR, PIN)
    return temperature

# Function to collect data for a specified duration and interval
def collect_data(duration_minutes, interval_seconds):
    data = []
    start_time = time.time()
    duration_seconds = duration_minutes * 60

    while time.time() - start_time < duration_seconds:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        temperature = read_temperature()
        data.append([timestamp, temperature])
        print(f"Timestamp: {timestamp}, Temperature: {temperature}°C")
        time.sleep(interval_seconds)

    return data

# Function to export data to Excel
def export_to_excel(data, filename):
    df = pd.DataFrame(data, columns=['Timestamp', 'Temperature'])
    df.to_excel(filename, index=False)
    print(f"Data saved to {filename}")

# Example usage
if __name__ == "__main__":
    duration_minutes = 5  # Set the duration in minutes
    interval_seconds = 10  # Set the interval in seconds
    data = collect_data(duration_minutes, interval_seconds)
    export_to_excel(data, 'temperature_data.xlsx')