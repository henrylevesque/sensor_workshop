import time
import math
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

# This is a quick test script to verify MAX4466 microphone + ADS1115 ADC is working.
# Press Ctrl+C to stop.

# Wiring: MAX4466 VCC→ADS1115 VDD→3.3V, MAX4466 GND→ADS1115 GND→GND, 
#         MAX4466 OUT→ADS1115 A0, ADS1115 SDA→GPIO2, ADS1115 SCL→GPIO3

SAMPLE_RATE = 500          # Mic sampling rate (Hz)
WINDOW_SIZE = 200          # Samples per dB reading
GAIN = 1                   # ADS gain (1 = ±4.096V)

# Setup ADS1115
def get_channel():
    """Initialize I2C and ADS1115 ADC"""
    i2c = busio.I2C(board.SCL, board.SDA)
    ads = ADS.ADS1115(i2c)
    ads.gain = GAIN
    return AnalogIn(ads, ADS.P0)

def read_db():
    """Read sound level in decibels"""
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

if __name__ == "__main__":
    print("=" * 70)
    print("SOUND SENSOR (ADS1115 + MAX4466) TEST")
    print("=" * 70)
    print("Reading sound level every 3 seconds...")
    print("Press Ctrl+C to stop.\n")
    
    reading_count = 0
    
    try:
        while True:
            reading_count += 1
            db_level = read_db()
            print(f"[{reading_count}] Sound Level: {db_level:.2f} dB")
            time.sleep(1)
    
    except KeyboardInterrupt:
        print("\n" + "=" * 70)
        print(f"Test stopped. {reading_count} readings taken.")
        print("=" * 70)
