import time
from datetime import datetime
try:
    import board
    import adafruit_dht
except Exception:
    board = None
    adafruit_dht = None

# This is a quick test script to verify DHT11 sensor is working.
# Press Ctrl+C to stop.

# Wiring: DHT11 S → GPIO 4, V → 3.3V, G → GND

try:
    if board is not None and adafruit_dht is not None:
        sensor = adafruit_dht.DHT11(board.D4)
    else:
        sensor = None
except Exception:
    sensor = None

def read_temperature():
    """Read temperature and humidity from DHT11"""
    if sensor is None:
        raise RuntimeError(
            "DHT11 sensor not initialized. Install libraries with:\n"
            "  sudo python3 -m pip install --break-system-packages adafruit-blinka\n"
            "  sudo python3 -m pip install --break-system-packages adafruit-circuitpython-dht"
        )
    
    try:
        temperature = sensor.temperature
        humidity = sensor.humidity
        return temperature, humidity
    except RuntimeError as e:
        return None, None

if __name__ == "__main__":
    print("=" * 70)
    print("DHT11 TEMPERATURE SENSOR TEST")
    print("=" * 70)
    print("Reading sensor data every 2 seconds...")
    print("Press Ctrl+C to stop.\n")
    
    reading_count = 0
    
    try:
        while True:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            temperature, humidity = read_temperature()
            
            if temperature is not None and humidity is not None:
                reading_count += 1
                print(f"[{reading_count}] {timestamp} | Temp: {temperature:.1f}°C | Humidity: {humidity:.1f}%")
            else:
                print(f"[FAILED] {timestamp} | Sensor read error, retrying...")
            
            time.sleep(2)
    
    except KeyboardInterrupt:
        print("\n" + "=" * 70)
        print(f"Test stopped. {reading_count} successful readings.")
        print("=" * 70)
