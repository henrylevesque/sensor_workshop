# Environmental Data Collection Workshop using Raspberry Pi Zero

Note: All scripts and examples in this repository are intended to run on a Raspberry Pi Zero 2 W with the appropriate sensors and libraries installed.

The goal of this repository is to provide directions, code, and documentation for running a workshop on using Raspberry Pi Zero to build sensors to collect environmental data.
# Environmental Data Collection Workshop using Raspberry Pi Zero

The goal of this repository is to provide directions, code, and documentation for running a workshop on using Raspberry Pi Zero to build sensors to collect environmental data.

## Navigation

For first time setup: [Directions for First Time Setup](Workshop.md)
For installation instructions and package setup: [Installation](INSTALL.md)
For information on Modules: [Sensors and Modules](Sensors.md)
For 3D printable enclosures: see the collection on [Printables.com](https://www.printables.com/@HenryLevesque/collections/1649941)

# Linux Commands for Raspberry Pi

## Basic Terminal Navigation

- `ls` - List files in current directory
- `cd [directory]` - Change directory
- `mkdir [name]` - Create new directory
- `rm [file]` - Remove file
- `rm -r [directory]` - Remove directory and contents
- `touch filename.txt` - Create a text file called `filename.txt` (to create a python file use `touch filename.py`)
- `nano filename.py` - Edit a file through terminal using nano
- `pwd` - Print working directory, useful for when using `scp` to transfer files
- `scp` - Use to copy files to and from the RPi

### Sudo

`sudo` stands for "SuperUser DO". It temporarily grants admin (root) privileges to execute commands that require elevated permissions. Always use caution with sudo commands.

Here's what you need to know about sudo:

1. **Purpose**: It allows regular users to execute commands with the security privileges of the superuser (root)
2. **Security**: Only users in the 'sudo' group can use sudo commands
3. **Password**: First sudo command requires password authentication (valid for 15 minutes)
4. **Common uses**:
   - Installing software (`sudo apt install`)
   - Updating system (`sudo apt update`)
   - Modifying system files (`sudo nano /etc/hostname`)
   - Hardware access (`sudo raspi-config`)

Best Practices:

- Double-check sudo commands before running them
- Only use sudo when necessary
- Never run sudo commands from untrusted sources
- Keep your sudo password private

## Package Management

```bash
# Update package list
sudo apt update

# Upgrade installed packages
sudo apt upgrade

# Install new package
sudo apt install [package-name]

# Remove package
sudo apt remove [package-name]
```

## Common Python Package Installation

```bash
# Install pip (Python package manager)
sudo apt install python3-pip

# Install common sensor libraries
sudo apt install python3-rpi.gpio
sudo pip3 install adafruit-circuitpython-dht
sudo apt install python3-pandas
sudo apt install python3-matplotlib
```

## Network Commands

```bash
# Check network connectivity
ping raspberrypi.local

# Connect via SSH
ssh [username]@[ip-address]

# Check IP address
hostname -I

# Check wireless status
iwconfig
```

## File Transfer Commands

```bash
# Copy from Raspberry Pi to local machine (run on your computer)
scp [username]@[ip-address]:/path/to/file /local/destination

# Copy from local machine to Raspberry Pi (run on your computer)
scp /path/to/local/file [username]@[ip-address]:/remote/destination
```

## Raspberry Pi Connect Setup - if not already installed on rpi os

1. On the Raspberry Pi:

```bash
# Download the Raspberry Pi Connect script
curl -L https://downloads.raspberrypi.com/connect_agent_v1.sh | bash

# Follow the prompts to complete setup
```

## Raspberry Pi Connect Setup - If using newer os versions with rpi-connect already installed

1. Turn on and sign in to Raspberry Pi connect:

```bash
# Turn on Raspberry Pi Connect
rpi-connect on

# Signin to Raspberry Pi Connect
rpi-connect signin

# Follow the prompts to complete setup
```

## Important System Commands

```bash
# Safely reboot
sudo reboot

# Safely shutdown
sudo shutdown -h now

# Check system temperature
vcgencmd measure_temp

# Check disk space
df -h
```

## File Editing

```bash
# Edit file with nano (beginner-friendly)
nano [filename]

# Basic nano commands:
# Ctrl + O : Save
# Ctrl + X : Exit
# Ctrl + W : Search
```
