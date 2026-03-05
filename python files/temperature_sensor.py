import time
import pandas as pd
from datetime import datetime
try:
    import board
    import adafruit_dht
except Exception:
    board = None
    adafruit_dht = None

# This script reads data from a DHT11 temperature sensor connected to a Raspberry Pi, collects the data for a specified duration and interval, and exports it to an Excel file.
# Text that follows the '#' symbol is a comment and is not executed as part of the code. It provides explanations and instructions for the user.

# INSTALLATION INSTRUCTIONS (run on Raspberry Pi):
# Step 1: Install pandas for Excel export
#   sudo apt install python3-pandas
# Step 2: Install CircuitPython libraries for DHT support
#   sudo python3 -m pip install adafruit-blinka
#   sudo python3 -m pip install adafruit-circuitpython-dht

# Wiring the Hardware
# Connect a Keyestudio DHT11 sensor to Raspberry Pi as follows:
# Keyestudio sensor pin labels (top to bottom on typical sensor):
#   S (Signal)  → GPIO 4 (Physical Pin 7)
#   V (VCC)     → 3.3V (Physical Pin 1)
#   G (GND)     → GND (Physical Pin 6)

# Create the DHT11 sensor object at GPIO 4 (board.D4 in CircuitPython notation)
try:
    if board is not None and adafruit_dht is not None:
        sensor = adafruit_dht.DHT11(board.D4)
    else:
        sensor = None
except Exception:
    sensor = None

# Function to read temperature and humidity data
def read_temperature():
    if sensor is None:
        raise RuntimeError(
            "DHT11 sensor not initialized. Install libraries with:\n"
            "  sudo python3 -m pip install adafruit-blinka adafruit-circuitpython-dht"
        )
    
    try:
        temperature = sensor.temperature
        humidity = sensor.humidity
        return temperature, humidity
    except RuntimeError as e:
        print(f"Sensor read error (retry): {e}")
        return None, None

# Function to collect data for a specified duration and interval
def collect_data(duration_minutes, interval_seconds):
    data = []
    start_time = time.time()
    duration_seconds = duration_minutes * 60

    while time.time() - start_time < duration_seconds:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        temperature, humidity = read_temperature()
        
        if temperature is not None and humidity is not None:
            data.append([timestamp, temperature, humidity])
            print(f"Timestamp: {timestamp}, Temperature: {temperature:.1f}°C, Humidity: {humidity:.1f}%")
        else:
            print(f"Timestamp: {timestamp}, Sensor read failed, retrying...")
        
        time.sleep(interval_seconds)

    return data

# Function to export data to Excel
def export_to_excel(data, filename):
    df = pd.DataFrame(data, columns=['Timestamp', 'Temperature (°C)', 'Humidity (%)'])
    df.to_excel(filename, index=False)
    print(f"Data saved to {filename}")

# Example usage
if __name__ == "__main__":
    duration_minutes = 5  # Set the duration in minutes
    interval_seconds = 10  # Set the interval in seconds
    data = collect_data(duration_minutes, interval_seconds)
    export_to_excel(data, 'temperature_data.xlsx')