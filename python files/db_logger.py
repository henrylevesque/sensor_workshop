import time
import math
import pandas as pd
from datetime import datetime
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

# This script reads sound level data from a microphone connected to an ADS1115 ADC on a Raspberry Pi, calculates the decibel level, and saves the output to an excel file.
# Text that follows the '#' symbol is a comment and is not executed as part of the code. It provides explanations and instructions for the user.

# This code requires pandas to export to an Excel file, to install pandas, run: sudo apt install python3-pandas
# This code requires the Adafruit ADS1x15 library, to install it, run: pip3 install adafruit-circuitpython-ads1x15

# STEP 1: Enable I2C on the Raspberry Pi
# Enter RPI config: sudo raspi-config → Navigate to: Interface Options → I2C → Enable 
# Then reboot the Pi: sudo reboot
# Verify I2C is working: sudo i2cdetect -y 1 You should see device address: 48


# STEP 2: Wiring the Hardware
# Connect MAX4466 Microphone to ADS1115 ADC, then connect ADS1115 to Raspberry Pi GPIO pins as follows:
# VCC → VDD → 3.3V (Pin 1)
# GND → GND → GND (Pin 6)
# OUT → A0 → GPIO2 / SDA (Pin 3)
# SCL → GPIO3 / SCL (Pin 5)
# ADDR → GND

SAMPLE_RATE = 500          # Mic sampling rate (Hz)
WINDOW_SIZE = 200          # Samples per dB reading
GAIN = 1                   # ADS gain

# Setup ADS1115
def get_channel():
    i2c = busio.I2C(board.SCL, board.SDA)
    ads = ADS.ADS1115(i2c)
    ads.gain = GAIN
    return AnalogIn(ads, ADS.P0)


def read_db():
    chan = get_channel()
    samples = []

    for _ in range(WINDOW_SIZE):
        samples.append(chan.voltage)
        time.sleep(1 / SAMPLE_RATE)

    mean = sum(samples) / len(samples)
    centered = [s - mean for s in samples]

    rms = math.sqrt(sum(s**2 for s in centered) / len(centered))

    if rms > 0:
        db = 20 * math.log10(rms / 4.096)
    else:
        db = -100

    return db


def collect_data(duration_minutes, interval_seconds):
    data = []
    start_time = time.time()
    duration_seconds = duration_minutes * 60

    while time.time() - start_time < duration_seconds:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        db_level = read_db()

        data.append([timestamp, db_level])
        print(f"Timestamp: {timestamp}, dB Level: {db_level:.2f}")

        time.sleep(interval_seconds)

    return data


def export_to_excel_file(data, filename):
    df = pd.DataFrame(data, columns=['Timestamp', 'Decibel Level (dB)'])
    df.to_excel(filename, index=False)
    print(f"Data saved to {filename}")


# -------- Example Usage --------
if __name__ == "__main__":
    duration_minutes = 5     # how long to run
    interval_seconds = 10    # how often to log

    data = collect_data(duration_minutes, interval_seconds)
    export_to_excel_file(data, 'sound_data.xlsx')