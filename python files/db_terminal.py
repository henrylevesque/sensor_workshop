import time
import math
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

# This script reads sound level data from a microphone connected to an ADS1115 ADC on a Raspberry Pi, calculates the decibel level, and prints it to the console. It continuously samples the sound level and updates the reading every few seconds.
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

SAMPLE_RATE = 500      # samples per second (max ~860 for ADS1115)
WINDOW_SIZE = 200      # samples per dB calculation
GAIN = 1               # ADS gain (1 = ±4.096V)

# Setup I2C + ADS1115 (kept near runtime)

def main():
    # Setup I2C + ADS1115
    i2c = busio.I2C(board.SCL, board.SDA)
    ads = ADS.ADS1115(i2c)
    ads.gain = GAIN
    chan = AnalogIn(ads, ADS.P0)

    print("Simple dB meter running... Press CTRL+C to stop.")

    while True:
        samples = []

        for _ in range(WINDOW_SIZE):
            samples.append(chan.voltage)
            time.sleep(1 / SAMPLE_RATE)

        # Remove DC bias
        mean = sum(samples) / len(samples)
        centered = [s - mean for s in samples]

        # Calculate RMS
        rms = math.sqrt(sum(s**2 for s in centered) / len(centered))

        if rms > 0:
            db = 20 * math.log10(rms / 4.096)  # 4.096V reference for gain=1
        else:
            db = -100

        print(f"Sound Level: {db:.2f} dB")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("Error:", e)