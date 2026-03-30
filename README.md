# Environmental Data Collection Workshop using Raspberry Pi Zero

**Goal**: Build Raspberry Pi Zero sensors to collect environmental data and export results in human-readable formats (Excel spreadsheets with timestamps).

**Note**: All scripts and examples in this workshop are intended to run on a Raspberry Pi Zero 2 W with appropriate sensors and libraries installed.

---

## Table of Contents

1. [Quick Start (No Git Required)](#quick-start-no-git-required)
2. [Getting Started](#getting-started)
3. [Required Materials](#required-materials)
4. [Required Software](#required-software)
5. [Setup Instructions](#setup-instructions)
6. [Hardware Wiring Guide](#hardware-wiring-guide)
7. [Running the Sensor Scripts](#running-the-sensor-scripts)
8. [Python Files Organization](#python-files-organization)
9. [Terminal Commands Reference](#terminal-commands-reference)
10. [WiFi Configuration](#wifi-configuration)
11. [File Transfer (scp)](#file-transfer-scp)
12. [Troubleshooting](#troubleshooting)
13. [Tips for First-Time Hardware Users](#tips-for-first-time-hardware-users)
14. [Project Planning Guidelines](#project-planning-guidelines)

---

## Quick Start (No Git Required)

**You don't need to clone anything or know git.** Follow these 3 steps to test a sensor and create your own files:

### Step 1: Test Your Sensor (Verify it Works)

Connect your sensor to the Pi, then run a test script:

```bash
# Connect via SSH first (see Setup Instructions below)
ssh pi@rpizero2w1.local

# Test temperature sensor
python3 temperature_test.py

# Watch output for 30 seconds, then press Ctrl+C to stop
# You should see real-time readings
```

**Available test scripts**:

- `python3 temperature_test.py` – DHT11 sensor
- `python3 motion_test.py` – PIR motion sensor
- `python3 sound_test.py` – Sound sensor with microphone

### Step 2: Understand the Data Format

Look at how the test script outputs data. This is what your real data collection should look like:

```
[1] 2026-03-05 10:30:45 | Temp: 22.5°C | Humidity: 45.2%
[2] 2026-03-05 10:30:47 | Temp: 22.6°C | Humidity: 45.1%
```

### Step 3: Create Your Own File and Collect Data

**No git clone needed.** Just create a file and paste code:

```bash
# Create an empty Python file
touch my_temperature_logger.py

# Open it in nano editor
nano my_temperature_logger.py
```

Now:

1. Go to the repo on GitHub: [https://github.com/henrylevesque/sensor_workshop](https://github.com/henrylevesque/sensor_workshop)
2. Open `temperature_data_logger.py` and copy all the code
3. Back in nano (on the Pi), right-click to paste the code
4. Press `Ctrl + O`, then `Enter` to save
5. Press `Ctrl + X` to exit

Now run your custom file:

```bash
python3 my_temperature_logger.py
```

**That's it!** You now have a working data logger saving to Excel.

---

## Getting Started

Before the workshop:

1. Familiarize yourself with this guide
2. Ensure you have the required software installed on your computer
3. Review the hardware components you'll be using
4. Have your Raspberry Pi flashed with Raspberry Pi OS and connected to WiFi

---

## Required Materials

**Provided by Workshop**:

- 3 Raspberry Pi Zero 2 W units (shared among groups)
- 3 Pi Sugar batteries (optional power supply)
- Sensors:
  - DHT11 temperature/humidity sensor (Keyestudio model)
  - HC-SR501 PIR motion sensor
  - Pi Camera module
  - Additional Keyestudio sensors available (see [All Available Sensors](#all-available-sensors))
- Basic electronics:
  - Jumper wires (male-to-female and male-to-male)
  - Breadboards
  - Resistors (various values)
- Micro SD cards (with Raspberry Pi OS pre-loaded)
- USB micro cables (for power and data transfer)

**You Should Have**:

- Computer (Mac, Linux, or Windows) with terminal access
- USB SD card reader (to prepare/modify SD cards if needed)
- Network connectivity for WiFi setup

---

## Required Software

**Essential**:

- [Raspberry Pi Imager](https://www.raspberrypi.com/software/) – to flash Raspberry Pi OS onto SD cards
- [Microsoft Excel](https://www.microsoft.com/en-us/microsoft-365/excel) or [LibreOffice Calc](https://www.libreoffice.org/) – to analyze data

**Recommended**:

- Terminal app (macOS/Linux) or PowerShell (Windows) – for SSH connection and file transfer
- [Microsoft Visual Studio Code](https://code.visualstudio.com/download) – for editing Python scripts remotely

**Optional (for data visualization)**:

- [ArcGIS Online](https://ucincinnati.maps.arcgis.com/home/index.html) – for geographic mapping
- [QGIS](https://qgis.org/download/) – open-source GIS software
- [Raspberry Pi Connect](https://connect.raspberrypi.com/sign-in) – for remote desktop access

---

## Setup Instructions

### Step 1: Flash Raspberry Pi OS

1. Download [Raspberry Pi Imager](https://www.raspberrypi.com/software/)
2. Insert your SD card into your computer's SD card reader
3. Open Raspberry Pi Imager and:
   - Choose **Device**: Raspberry Pi Zero 2 W
   - Choose **OS**: Raspberry Pi OS Lite (smallest option, recommended for beginners)
   - Choose **Storage**: Your SD card
   - Click **Edit Settings**:
     - Set hostname: `rpizero2w1` (or another name)
     - Enable SSH with password authentication
     - Set WiFi SSID and password (same network as your computer)
     - Set locale and timezone
   - Click **Write** and wait to complete

### Step 2: Connect to Your Raspberry Pi

**From Mac/Linux**:

```bash
ssh pi@rpizero2w1.local
```

**From Windows (PowerShell)**:

```powershell
ssh pi@rpizero2w1
```

Default password: `raspberry` (unless you changed it during setup)

### Step 3: Install Required Python Libraries

Once connected to your Raspberry Pi, run:

```bash
# Update package lists
sudo apt update

# Install pandas (for Excel export)
sudo apt install python3-pandas

# Install CircuitPython libraries for sensors
sudo python3 -m pip install --break-system-packages adafruit-blinka
sudo python3 -m pip install --break-system-packages adafruit-circuitpython-dht

# Optional: install matplotlib for graphing
sudo apt install python3-matplotlib
```

---

## Hardware Wiring Guide

### Raspberry Pi Pinout Reference

The Raspberry Pi has 40 GPIO (General Purpose Input/Output) pins. Understand the difference between:

- **GPIO number** (e.g., GPIO 4) – used in Python code
- **Physical pin number** (e.g., Pin 7) – physical location on the board

**Common pins you'll use**:

- **3.3V**: Physical Pin 1
- **5V**: Physical Pin 2
- **GND**: Physical Pins 6, 9, 14, 20, 25, 30, 34, 39
- **I2C SDA**: GPIO 2 (Physical Pin 3)
- **I2C SCL**: GPIO 3 (Physical Pin 5)

Always refer to a [Raspberry Pi pinout diagram](https://www.raspberrypi.com/documentation/computers/raspberry-pi.html) when wiring.

### Temperature Sensor (DHT11 - Keyestudio)

**Sensor Pin Labels** (top to bottom):

- `S` (Signal/DATA)
- `V` (VCC/Power)
- `G` (GND/Ground)

**Wiring**:

| Sensor Pin   | → | Raspberry Pi            |
| ------------ | -- | ----------------------- |
| `V` (VCC)  | → | 3.3V (Physical Pin 1)   |
| `G` (GND)  | → | GND (Physical Pin 6)    |
| `S` (DATA) | → | GPIO 4 (Physical Pin 7) |

**Code**: `temperature_sensor.py`

**Run**:

```bash
python3 temperature_sensor.py
```

**Output**: `temperature_data.xlsx` (with timestamp, temperature, humidity)

### PIR Motion Sensor (HC-SR501)

**Sensor Pin Labels**:

- `VCC` (Power)
- `OUT` (Output/Signal)
- `GND` (Ground)

**Wiring**:

| Sensor Pin | → | Raspberry Pi              |
| ---------- | -- | ------------------------- |
| `VCC`    | → | 5V (Physical Pin 2)       |
| `GND`    | → | GND (Physical Pin 6)      |
| `OUT`    | → | GPIO 23 (Physical Pin 16) |

**Code**: `pir_motion_sensor.py`

**Run**:

```bash
python3 pir_motion_sensor.py
```

**Output**: `motion_data.xlsx` (with timestamp, motion detected true/false)

### PI Camera Module

**Connected via ribbon cable** to the Camera port on the Raspberry Pi.

**Code**: `capture_images.py`

**Run**:

```bash
python3 "python files/capture_images.py"
```

**Output**: Images saved to `captured_images/` folder

### Sound/Microphone Sensor (ADS1115 ADC + MAX4466)

**ADC Module**: ADS1115 (converts analog to digital)

**Wiring**:

| Component    | → | Raspberry Pi   |
| ------------ | -- | -------------- |
| MAX4466 VCC  | → | ADS1115 VDD    |
| MAX4466 GND  | → | ADS1115 GND    |
| MAX4466 OUT  | → | ADS1115 A0     |
| ADS1115 SDA  | → | GPIO 2 (Pin 3) |
| ADS1115 SCL  | → | GPIO 3 (Pin 5) |
| ADS1115 ADDR | → | GND (Pin 6)    |

**Enable I2C on Raspberry Pi** (required for ADC):

```bash
sudo raspi-config
# Navigate: Interface Options → I2C → Enable
# Reboot: sudo reboot
```

**Code**: `db_logger.py` (saves to Excel) or `db_terminal.py` (prints to console)

---

## Running the Sensor Scripts

### Basic Structure

All sensor scripts follow the same pattern:

1. **Import libraries** at the top
2. **Define configuration** (pins, durations)
3. **Collect data** at set intervals for a set duration
4. **Export to Excel** with timestamp and sensor readings

### Configurable Parameters

Edit the bottom of any script to change:

```python
if __name__ == "__main__":
    duration_minutes = 5    # How long to collect data
    interval_seconds = 10   # Time between readings
    filename = "temperature_data.xlsx"  # Output file
```

### Data Protection: Append Mode

All sensor scripts now **append data directly to Excel files** as readings are collected. This means:

- **No data loss if power fails**: Each reading is saved immediately
- **Longer collection periods**: Run the Pi overnight without fear of losing all data
- **Safe battery operation**: If the battery dies mid-collection, all previous readings are safely saved
- **Continuous operation**: Can run the script again to resume collection (data appends to existing file)

### Example Usage

**Temperature sensor for 10 minutes, reading every 30 seconds**:

```bash
# Edit the script
nano temperature_sensor.py

# Change:
# duration_minutes = 10
# interval_seconds = 30

# Save and exit, then run:
python3 temperature_sensor.py
```

**Monitoring**:

- Watch readings print to the terminal as they're collected
- When complete, an Excel file is created with all data + timestamps
- Download the file to your computer using `scp` (see [File Transfer](#file-transfer-scp))

---

## Python Files Organization

### File Structure

This repository contains **test scripts** (for quick demos) and **data logger scripts** (for actual data collection):

| Category              | File                           | Sensor            | Use                                      |
| --------------------- | ------------------------------ | ----------------- | ---------------------------------------- |
| **Test**        | `temperature_test.py`        | DHT11             | Verify sensor works (prints to terminal) |
| **Test**        | `motion_test.py`             | PIR motion        | Verify sensor works (prints to terminal) |
| **Test**        | `sound_test.py`              | MAX4466 + ADS1115 | Verify sensor works (prints to terminal) |
| **Data Logger** | `temperature_data_logger.py` | DHT11             | Collect data to Excel (append mode)      |
| **Data Logger** | `motion_data_logger.py`      | PIR motion        | Collect data to Excel (append mode)      |
| **Data Logger** | `sound_data_logger.py`       | MAX4466 mic       | Collect data to Excel (append mode)      |
| **Camera**      | `capture_images.py`          | Pi Camera         | Take photos to folder                    |
| **Template**    | `*_TEMPLATE.py` files        | Various           | Examples for other sensors               |

### Recommended Student Workflow

**Step 1: Test the sensor works**

```bash
python3 temperature_test.py
# Watch output for 30 seconds, press Ctrl+C
```

**Step 2: Use demo script to understand output format**

- See what kind of data your sensor produces
- Understand the timing and format

**Step 3: Run data collection with your own params**

```bash
# Edit the data logger file to set duration
nano temperature_data_logger.py

# Change these lines:
# duration_minutes = 60    # Run for 1 hour instead of 5 minutes
# interval_seconds = 30    # Read every 30 seconds instead of 10

# Save (Ctrl+O, Enter) and exit (Ctrl+X)
python3 temperature_data_logger.py
```

### Creating Your Own Scripts

Students can write their own scripts using the provided files as templates. Here's the easiest workflow:

#### Method 1: Copy and Modify Existing File

```bash
# Copy the temperature data logger as a starting point
cp temperature_data_logger.py my_custom_sensor.py

# Edit your copy
nano my_custom_sensor.py
```

#### Method 2: Create and Edit a New File

```bash
# Create an empty Python file
touch my_sensor.py

# Open it in nano editor
nano my_sensor.py
```

**In nano editor**:

1. You can copy/paste code from any source (this repo or your own code)
2. Edit as needed
3. Save: Press `Ctrl + O`, then `Enter`
4. Exit: Press `Ctrl + X`

**Tips for using nano**:

- Right-click to paste (if using terminal on Windows/Mac)
- Use arrow keys to move around
- `Ctrl + A` = beginning of line
- `Ctrl + E` = end of line
- `Ctrl + W` = search
- `Ctrl + K` = delete line

#### Example: Write Your Own Temperature Logger

```bash
# Create new file
touch my_temp_logger.py

# Open in nano
nano my_temp_logger.py

# Now paste this code (or type it):
```

Then paste:

```python
import time
from datetime import datetime
import board
import adafruit_dht
from openpyxl import Workbook, load_workbook
import os

# Your custom temperature logger
sensor = adafruit_dht.DHT11(board.D4)

def init_excel_file(filename):
    if not os.path.exists(filename):
        wb = Workbook()
        ws = wb.active
        ws.append(["Timestamp", "Temp", "Humidity"])
        wb.save(filename)

def append_to_excel(filename, timestamp, temp, humidity):
    wb = load_workbook(filename)
    ws = wb.active
    ws.append([timestamp, temp, humidity])
    wb.save(filename)

if __name__ == "__main__":
    init_excel_file("my_data.xlsx")
    for i in range(10):  # 10 readings
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        temp = sensor.temperature
        humidity = sensor.humidity
        append_to_excel("my_data.xlsx", ts, temp, humidity)
        print(f"[{i+1}] {ts} | {temp}°C | {humidity}%")
        time.sleep(5)
```

Then save and exit nano.

### Template Files for Other Sensors

If you want to use sensors **not covered by the main scripts**, template files are provided:

- `light_test_TEMPLATE.py` – Light sensor template
- `soil_moisture_test_TEMPLATE.py` – Soil moisture sensor template
- `distance_test_TEMPLATE.py` – Ultrasonic distance sensor template

**To use a template**:

1. Copy it to a real file: `cp light_test_TEMPLATE.py light_test.py`
2. Edit it: `nano light_test.py`
3. Customize the GPIO pins and sensor parameters
4. Test it: `python3 light_test.py`

---

## Terminal Commands Reference

### Basic Navigation

```bash
# List files in current directory
ls

# Change directory
cd [directory_name]

# Go to home directory
cd ~

# Go back one directory
cd ..

# Print current directory path
pwd

# Make a new directory
mkdir [folder_name]

# Remove a file
rm [file_name]

# Remove a directory and all contents (BE CAREFUL!)
rm -r [directory_name]

# View file contents
cat [file_name]

# Edit file
nano [file_name]
```

### File Operations

```bash
# Create an empty file
touch [filename.txt]

# Copy a file
cp [source] [destination]

# Move or rename a file
mv [old_name] [new_name]

# Check file size/permissions
ls -lh [filename]
```

### Python Commands

```bash
# Check Python version
python3 --version

# Run a Python script
python3 [script_name.py]

# Install a Python package
sudo python3 -m pip install [package_name]

# Install with system package override (for workshop use)
sudo python3 -m pip install --break-system-packages [package_name]

# List installed packages
python3 -m pip list
```

### System Commands

```bash
# Safely reboot the Raspberry Pi
sudo reboot

# Safely shut down
sudo shutdown -h now

# Check system temperature
vcgencmd measure_temp

# Check disk space
df -h

# Check WiFi connection
hostname -I

# Ping (test connection)
ping [hostname.local]
```

### Understanding sudo

`sudo` = "SuperUser DO" – runs commands with administrator privileges (use with caution!)

**When to use sudo**:

- Installing software (`sudo apt install`)
- Modifying system files (`sudo nano /etc/hostname`)
- Hardware configuration (`sudo raspi-config`)

**Best practices**:

- Only use when necessary
- Double-check the command before pressing Enter
- Never run sudo commands from untrusted sources

---

## WiFi Configuration

### Connect to a Different Network (headless-first, then fallbacks)

This recipe assumes the Pi was flashed with WiFi set in the imager and is currently reachable headless over that initial 2.4 GHz hotspot. Students should connect their laptop to the same 2.4 GHz hotspot (the one used during imaging) to SSH in, then add their home hotspot credentials.

Most-likely-to-work (do these first)

1. SSH into the Pi from your laptop (make sure the laptop is on the same 2.4 GHz hotspot used during imaging):

```bash
ssh pi@rpizero2w1.local
# or use the Pi's IP address shown by the imager
```

2. Edit the system `wpa_supplicant` file and add your home network. The Pi Zero 2 W only supports 2.4 GHz, so use a 2.4 GHz SSID.

```bash
sudo nano /etc/wpa_supplicant/wpa_supplicant.conf
```

Make sure the file contains this header and your network block (set `country=`):

```conf
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=US

network={
    ssid="YourHomeSSID"
    psk="YourHomePassword"
    priority=1
    scan_ssid=1
}
```

*Note on `priority`: Only matters if multiple networks are in this file. Higher numbers connect first. If you add a second network, use `priority=2` or higher for it to de-prioritize.*

*Note on `scan_ssid=1`: Include this if your network is hidden OR if you have a weak signal or problematic router; it increases robustness.*

Save (Ctrl+O, Enter) and exit (Ctrl+X).

3. Apply the new settings (this reloads wpa_supplicant without reboot):

```bash
sudo wpa_cli -i wlan0 reconfigure
# Wait ~10 seconds then check IP
hostname -I || ip addr show wlan0
```

4. **Verify the connection worked**:
   - If `hostname -I` shows a different IP address (not on the imaging hotspot's range), the Pi is now connected to your home network.
   - Disconnect your laptop from the imaging hotspot and connect to your home network.
   - SSH to the Pi using its new IP or mDNS name (usually `rpizero2w1.local`):
   
```bash
ssh pi@rpizero2w1.local
# or use the IP shown by hostname -I
```

If the Pi connects successfully, you're done. If it shows no IP or the old IP, continue to the troubleshooting section below.

Important headless notes
- The initial hotspot created during imaging is only used to SSH in to the Pi once. After you add your home network to `/etc/wpa_supplicant/wpa_supplicant.conf` and reload, the Pi will attempt to join the added networks automatically.
- The Pi Zero 2 W does not support 5 GHz — ensure your home SSID is broadcasting on 2.4 GHz or that the router has a combined SSID that includes 2.4 GHz.

If the simple reload didn't work (fallbacks and diagnostics)

5. Quick file checks and fixes (run these once):

```bash
# Remove Windows CRLF line endings if file was edited on Windows
sudo sed -i 's/\r$//' /etc/wpa_supplicant/wpa_supplicant.conf

# Ensure correct owner & restrictive permissions
sudo chown root:root /etc/wpa_supplicant/wpa_supplicant.conf
sudo chmod 600 /etc/wpa_supplicant/wpa_supplicant.conf
```

6. Try restarting services (try both wpa_supplicant forms since some installs use the per-interface unit):

```bash
sudo systemctl restart wpa_supplicant || sudo systemctl restart wpa_supplicant@wlan0
sudo systemctl restart dhcpcd || echo "dhcpcd may not be installed on this image"
```

7. If `dhcpcd` restart reports "Unit not found" or you still have no IP, check which network manager is active and view logs:

```bash
systemctl is-active NetworkManager || systemctl is-active systemd-networkd || echo "No NetworkManager/systemd-networkd active"
which dhcpcd || dpkg -l | grep dhcpcd
sudo journalctl -u wpa_supplicant --no-pager -n 200
sudo journalctl -u dhcpcd --no-pager -n 200
ps aux | grep -E 'dhcpcd|wpa_supplicant|NetworkManager|systemd-networkd'
```

8. Alternatives and useful commands
- Use `wpa_passphrase` to append a hashed PSK (avoids storing plain text):

```bash
wpa_passphrase "YourHomeSSID" "YourHomePassword" | sudo tee -a /etc/wpa_supplicant/wpa_supplicant.conf
```

- If the system uses NetworkManager (uncommon on Raspberry Pi OS Lite), connect using `nmcli` from the Pi:

```bash
nmcli device wifi connect "YourHomeSSID" password "YourHomePassword"
```

What to collect and paste here if it still fails

```bash
sudo systemctl status dhcpcd --no-pager
sudo journalctl -u dhcpcd --no-pager -n 200
sudo journalctl -u wpa_supplicant --no-pager -n 200
ip addr show wlan0
hostname -I
sudo cat /etc/wpa_supplicant/wpa_supplicant.conf
```

---

## File Transfer (scp)

Transfer data files and scripts between your computer and the Raspberry Pi.

### Prerequisites

1. Raspberry Pi is powered on and connected to WiFi
2. Get your Pi's hostname or IP: `hostname -I` (on the Pi)
3. You're running the command from your computer's terminal

### Download Data FROM Raspberry Pi

**Mac/Linux**:

```bash
scp pi@rpizero2w1.local:/home/pi/temperature_data.xlsx ~/Desktop/
```

**Windows (PowerShell)**:

```powershell
scp pi@rpizero2w1:/home/pi/temperature_data.xlsx C:\Users\YourUsername\Desktop\
```

### Upload Script TO Raspberry Pi

**Mac/Linux**:

```bash
scp ~/Desktop/my_script.py pi@rpizero2w1.local:/home/pi/
```

**Windows (PowerShell)**:

```powershell
scp C:\Users\YourUsername\Desktop\my_script.py pi@rpizero2w1:/home/pi/
```

### Common Examples

| Action               | Mac/Linux                                                             | Windows                                                                             |
| -------------------- | --------------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| Download temp data   | `scp pi@rpizero2w1.local:/home/pi/temperature_data.xlsx ~/Desktop/` | `scp pi@rpizero2w1:/home/pi/temperature_data.xlsx C:\Users\YourUsername\Desktop\` |
| Download motion data | `scp pi@rpizero2w1.local:/home/pi/motion_data.xlsx ~/Downloads/`    | `scp pi@rpizero2w1:/home/pi/motion_data.xlsx C:\Users\YourUsername\Downloads\`    |
| Upload edited script | `scp ~/my_script.py pi@rpizero2w1.local:/home/pi/`                  | `scp C:\Users\YourUsername\my_script.py pi@rpizero2w1:/home/pi/`                  |
| Download all images  | `scp -r pi@rpizero2w1.local:/home/pi/captured_images/ ~/Desktop/`   | `scp -r pi@rpizero2w1:/home/pi/captured_images/ C:\Users\YourUsername\Desktop\`   |

### Notes

- Replace `YourUsername` with your actual Windows username
- Use `rpizero2w1.local` (Mac/Linux) or `rpizero2w1` (Windows) – try both if one doesn't work
- Default password: `raspberry`
- The `:` (colon) separates remote address from file path
- Use `-r` flag to copy entire folders

---

## Running Data Loggers Persistently (Without SSH attached)

By default, if you SSH into the Pi, start a data logger script, and then disconnect SSH, the script will stop. To keep a logger running after you disconnect:

### Quick Method: Use `nohup` and background the process

Start the logger in the background with output redirected to a file:

```bash
nohup python3 temperature_data_logger.py >/home/pi/temp_log.txt 2>&1 &
```

Notes:
- `nohup` makes the process ignore disconnect signals (SIGHUP)
- Output is written to `/home/pi/temp_log.txt` (change filename as needed)
- The logger data (Excel file) is written to the path specified in the script
- You can safely disconnect SSH; the script continues running

### Alternative: Start then `disown` the process

If you already started the script directly:

```bash
python3 temperature_data_logger.py >/home/pi/temp_log.txt 2>&1 &
jobs
disown -h %1    # prevents SIGHUP for job %1
# now disconnect SSH
```

### Monitor or stop the running logger

```bash
# Check if it's still running
pgrep -a -f temperature_data_logger.py

# View the log output
tail -f /home/pi/temp_log.txt

# Stop the logger (keyboard interrupt won't work after disconnect)
pkill -f temperature_data_logger.py
```

### Reconnect and copy results

```bash
# SSH back in
ssh pi@rpizero2w3

# Copy the Excel file to your Windows machine
# (run from PowerShell on Windows)
scp pi@rpizero2w3:/home/pi/temperature_data.xlsx C:\Users\leves\Downloads\
```

---

## Troubleshooting

### Camera not detected

If your Raspberry Pi camera (official module or compatible CSI camera like Arducam) is not detected, first check:

1. **Physical connection**: Ensure the ribbon cable is fully inserted into the Camera CSI port (not the Display DSI port).
2. **Check camera detection at boot**:

```bash
# List detected cameras
rpicam-hello --list-cameras
# or (older systems)
v4l2-ctl --list-devices
# Check kernel messages for camera errors
dmesg | grep -iE 'camera|imx|ov5|arducam'
```

If the camera is not listed, it may be due to a forced or conflicting device-tree overlay. Apply these fixes:

3. Back up and remove any forced overlays that conflict with auto-detection:

```bash
sudo cp /boot/firmware/config.txt /boot/firmware/config.txt.bak
sudo sed -i '/^camera_auto_detect=0/d; /^dtoverlay=imx219/d; /^dtoverlay=arducam/d' /boot/firmware/config.txt
```

4. Ensure I2C probing is enabled (add if missing):

```bash
# Check if this line exists in /boot/firmware/config.txt
grep "dtparam=i2c_arm=on" /boot/firmware/config.txt
# If not found, add it:
sudo sed -i '/^\[all\]/a dtparam=i2c_arm=on' /boot/firmware/config.txt
```

5. Reboot and verify:

```bash
sudo reboot
# after reboot, check if camera is now detected
rpicam-hello --list-cameras
# Check I2C bus for camera device
sudo i2cdetect -l
sudo i2cdetect -y 1      # standard camera I2C bus
```

If the camera now appears in `rpicam-hello --list-cameras`, you're good to run the image test and logger scripts in `python files/`.

### Cannot Connect via SSH

**Problem**: `ssh: Could not resolve hostname rpizero2w1.local`

**Solutions**:

1. Check if Raspberry Pi is on and connected to WiFi

   ```bash
   # On the Pi
   hostname -I
   ```
2. Try using IP address directly:

   ```bash
   ssh pi@192.168.1.100
   ```
3. Try `rpizero2w1` without `.local` on Windows:

   ```powershell
   ssh pi@rpizero2w1
   ```

### Python Module Not Found

**Problem**: `ModuleNotFoundError: No module named 'adafruit_dht'`

**Solution**:

```bash
sudo apt update
sudo python3 -m pip install --break-system-packages adafruit-blinka
sudo python3 -m pip install --break-system-packages adafruit-circuitpython-dht
```

### Sensor Returns None or No Data

**Possible causes**:

1. **Wiring issue**: Double-check all connections match the wiring diagram
2. **Sensor dead/damaged**: Try another sensor of the same model
3. **Power issue**: Check if 3.3V and GND are properly connected
4. **I2C not enabled** (for ADS1115): Run `sudo raspi-config` → Interface Options → I2C → Enable

### Excel File Not Created

**Problem**: Script runs but no `.xlsx` file appears

**Solution**:

1. Check current directory:

   ```bash
   ls -la
   ```

   Files should appear in the same folder as the script
2. Verify pandas is installed:

   ```bash
   python3 -c "import pandas; print('OK')"
   ```
3. Check for permission errors:

   ```bash
   chmod 755 temperature_sensor.py
   ```

### WiFi Disconnects Frequently

**Problem**: Raspberry Pi keeps losing WiFi connection

**Solution**:

1. Edit config to prioritize speed:

   ```bash
   sudo nano /etc/wpa_supplicant/wpa_supplicant.conf
   ```
2. Add to your network block:

   ```
   network={
       ssid="YourNetwork"
       psk="YourPassword"
       priority=1
       scan_ssid=1
   }
   ```
3. Restart:

   ```bash
   sudo systemctl restart dhcpcd
   ```

### Battery Draining Quickly

**Problem**: Pi Sugar battery dies during long data collection

**Solutions**:

1. Use screen blanking to save power:

   ```bash
   # Disable HDMI
   tvservice -o
   ```
2. Collect data in shorter bursts (modify duration_minutes in script)
3. Transfer data frequently to backup

---

## Tips for First-Time Hardware Users

### Understanding GPIO Pins

- **GPIO** = General Purpose Input/Output
- Think of pins as "switches" that can read (input) or control (output) voltages
- Each pin has a **GPIO number** (used in code) and **physical pin number** (physical location)
- **Always check a pinout diagram** before connecting anything

**Example**: GPIO 4 is the 7th pin on the board. The code uses GPIO 4, but you physically wire to Pin 7.

### Preventing Damage

1. **Turn off power** before changing wires
2. **Check twice before powering on** – wrong connections can break sensors
3. **Use 3.3V, not 5V, for digital inputs** – most sensors will die at 5V
4. **Don't let wires touch** – prevents short circuits
5. **Keep the workspace clean** – no liquids near electronics

### Working with Breadboards

- **Red rail**: Power (3.3V or 5V)
- **Black/Blue rail**: Ground (GND)
- **Column holes**: All holes in a column are connected

### Testing Incrementally

1. **Wire one component at a time**
2. **Test before adding the next**
3. **Check output at each step** (print sensor readings to terminal first)
4. **Save working code** before making changes

### Reading Sensor Data

- **Temperature**: In Celsius (°C) by default
- **Humidity**: Percentage (0-100%)
- **Motion**: True (detected) or False (not detected)
- **Image**: Raw pixel data in binary format

### Battery Life Tips

- **DHT11 sensor**: Very low power (~2mA)
- **PIR sensor**: Low power (~65mA)
- **Camera**: High power (~200mA+) – use sparingly
- **Raspberry Pi idle**: ~100-150mA with WiFi
- **Typical battery life**: 8-12 hours continuous use

---

## Project Planning Guidelines

### Choose Your Phenomena

**Good choices** (measurable in 1 week):

- Temperature changes over time
- Motion patterns in a room
- Light levels at different times of day
- Humidity in a storage area
- Sound levels in a location

**Not recommended**:

- Weather (need professional equipment)
- Pollution levels (need certified sensors)
- Seismic activity (need expensive sensors)

### Ethical Data Collection

1. **Get permission** before collecting data on/near people
2. **Avoid areas with privacy concerns** (someone's home, bathroom, etc.)
3. **Document your location** so others can verify your methodology
4. **Explain your research goal** to anyone who asks
5. **Destroy data after analysis** if containing personal information

### Data Collection Plan

**Before you start**, document:

- **Location**: Specific address or GPS coordinates
- **Duration**: How long you'll collect data
- **Interval**: How often you'll take readings
- **Sensor**: Which sensors you're using
- **Goal**: What question are you answering?

### Working with Long-Term Data

If your battery might die before collection ends:

1. **Export data periodically**:

   - Every hour, download the Excel file via `scp`
   - Keep copies on your computer
2. **Use the append feature**:

   - Scripts are updated to append new data to existing files
   - If the Pi restarts, data continues in the same file
   - No data loss if battery dies mid-collection
3. **Backup important data**:

   ```bash
   # Download files before battery dies
   scp pi@rpizero2w1:/home/pi/*.xlsx ~/Backup/
   ```

---

## 3D Printable Enclosures

Check out [Printables.com collection](https://www.printables.com/@HenryLevesque/collections/1649941) for weatherproof sensor housings.

---

## All Available Sensors

The Keyestudio sensor kit includes:

- Capacitive Touch
- PIR Motion ✓ (covered in this guide)
- Linear Temperature
- Collision Sensor
- Soil Moisture
- Photocell (light sensor)
- Water Level
- Analog Rotation (potentiometer)
- Analog Temperature
- Flame Alarm
- Knock Sensor
- IR Obstacle Avoidance
- Analog Ceramic Vibration
- Ultrasound (distance)
- Rotary Encoder
- Temperature & Humidity Display ✓ (DHT11, covered in this guide)
- Steam Moisture
- Analog Sound ✓ (covered in this guide)
- Joystick
- 4-digit LED Digital Tube
- White LED
- Passive Buzzer
- Active Buzzer
- Digital IR Receiver
- Digital IR Transmitter
- Button
- Reed Switch
- Line Tracking
- Traffic Light
- Hall Sensor
- Motor Module
- Pulse Rate Monitor
- Single Relay
- Digital Tilt
- Voltage Detection
- RGB LED

---

## Quick Reference Cheat Sheet

| Task               | Command                                                              |
| ------------------ | -------------------------------------------------------------------- |
| Connect via SSH    | `ssh pi@rpizero2w1.local` (Mac) or `ssh pi@rpizero2w1` (Windows) |
| Edit WiFi          | `sudo nano /etc/wpa_supplicant/wpa_supplicant.conf`                |
| Install libraries  | `sudo python3 -m pip install --break-system-packages [package]`    |
| Run sensor script  | `python3 temperature_sensor.py`                                    |
| Download data      | `scp pi@rpizero2w1.local:/home/pi/*.xlsx ~/Desktop/` (Mac)         |
| Check IP           | `hostname -I`                                                      |
| Safely shutdown    | `sudo shutdown -h now`                                             |
| Check temperatures | `vcgencmd measure_temp`                                            |

---

## Need Help?

1. **Check this guide** – most issues are covered in [Troubleshooting](#troubleshooting)
2. **Check sensor wiring** – most problems are connection-related
3. **Verify libraries are installed** – run install commands again
4. **Test incrementally** – wire one sensor, test it, then add the next
5. **Ask the instructor** – we're here to help!
