# Installation guide

This project contains Python scripts for Raspberry Pi sensors. Follow the steps below on your Raspberry Pi (or in a suitable Python environment) to prepare the system.

1) Update the system (run on the Pi)

```sh
sudo apt update; sudo apt upgrade -y
```

2) Install system packages (on Raspberry Pi OS)

```sh
sudo apt install -y i2c-tools python3-smbus libportaudio2
```

3) Install Python packages (pip)

```sh
pip3 install -r requirements-pip.txt
```

4) Camera note

The `capture_images.py` script uses `libcamera-still`. On modern Raspberry Pi OS versions, install the libcamera apps if they are not present:

```sh
sudo apt install -y libcamera-apps
```

5) Optional: enable I2C and camera in `raspi-config` if using those interfaces

```sh
sudo raspi-config
# Navigate to Interface Options -> enable I2C and Camera
```

6) Run a script

```sh
python3 "python files/temperature_sensor.py"
python3 "python files/pir_motion_sensor.py"
python3 "python files/capture_images.py"
```
