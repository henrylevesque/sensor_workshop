import time
from datetime import datetime

# TEMPLATE FILE: Soil Moisture Sensor Test
# This is a template for reading soil moisture using an analog sensor and ADS1115 ADC.
# Modify this based on your specific sensor setup.

# Sensor Type: Capacitive or resistive soil moisture sensor with ADS1115 ADC
# Wiring:
# - Moisture sensor VCC → 3.3V
# - Moisture sensor GND → GND
# - Moisture sensor AO (analog output) → ADS1115 A1 (change A1 if using different pin)
# - ADS1115 SDA → GPIO 2 (Pin 3)
# - ADS1115 SCL → GPIO 3 (Pin 5)

import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

# Initialize I2C and ADS1115
i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c)
ads.gain = 1

# Change A1 to A0, A2, or A3 if your sensor is on a different ADS pin
channel = AnalogIn(ads, ADS.P1)

def read_moisture():
    """Read raw voltage and convert to moisture percentage"""
    voltage = channel.voltage
    # Calibration: Adjust these values based on dry/wet testing
    # DRY: ~3.3V, WET: ~0.5V (typical values, yours may differ)
    dry_voltage = 3.3
    wet_voltage = 0.5
    
    moisture_percent = 100 * (dry_voltage - voltage) / (dry_voltage - wet_voltage)
    moisture_percent = max(0, min(100, moisture_percent))  # Clamp 0-100%
    
    return moisture_percent, voltage

print("=" * 70)
print("SOIL MOISTURE SENSOR TEST")
print("=" * 70)
print("Reading soil moisture every 2 seconds...")
print("Press Ctrl+C to stop.\n")

reading_count = 0

try:
    while True:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        moisture, voltage = read_moisture()
        
        reading_count += 1
        print(f"[{reading_count}] {timestamp} | Moisture: {moisture:.1f}% | Voltage: {voltage:.2f}V")
        
        time.sleep(2)

except KeyboardInterrupt:
    print("\n" + "=" * 70)
    print(f"Test stopped. {reading_count} readings.")
    print("=" * 70)

# TIPS FOR STUDENTS:
# - Calibrate by testing in completely dry soil and completely wet soil
# - Adjust dry_voltage and wet_voltage based on your readings
# - Use this test to find exact voltage ranges, then update the numbers
# - Different soil types have different moisture levels
