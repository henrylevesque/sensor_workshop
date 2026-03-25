import time
from datetime import datetime
import subprocess
import shutil

# This is a quick test script to verify the camera is working.
# Press Ctrl+C to stop.

# Camera support: Raspberry Pi Camera Module or compatible CSI camera
# Requires libcamera (rpicam-apps/libcamera-apps) to be installed on the system
#
# NOTE: If the camera is not detected:
# 1. Check physical connection: ribbon cable fully inserted into Camera CSI port
# 2. Check for forced overlays in /boot/firmware/config.txt:
#    Remove lines like `camera_auto_detect=0`, `dtoverlay=imx219`, `dtoverlay=arducam`
# 3. Ensure I2C is enabled (add if missing in /boot/firmware/config.txt):
#    dtparam=i2c_arm=on
#
# Quick fix (run on the Pi and reboot):
#   sudo cp /boot/firmware/config.txt /boot/firmware/config.txt.bak
#   sudo sed -i '/^camera_auto_detect=0/d; /^dtoverlay=imx219/d; /^dtoverlay=arducam/d' /boot/firmware/config.txt
#   sudo sed -i '/^\[all\]/a dtparam=i2c_arm=on' /boot/firmware/config.txt
#   sudo reboot
#


def get_camera_command():
    """Return available still-image camera command for this OS."""
    for cmd in ("rpicam-still", "libcamera-still"):
        if shutil.which(cmd) is not None:
            return cmd

    raise EnvironmentError(
        "No camera capture command found. Install one of:\n"
        "  sudo apt update\n"
        "  sudo apt install -y rpicam-apps   # Raspberry Pi OS Bookworm/newer (recommended)\n"
        "  sudo apt install -y libcamera-apps # Raspberry Pi OS Bullseye/older\n"
        "Note: Ensure the camera is physically connected and detected (see README)."
    )

def test_camera():
    """Test if camera is working by capturing a test image"""
    camera_cmd = get_camera_command()
    
    try:
        # Capture a test image to /dev/null (doesn't save it)
        subprocess.run(
            [camera_cmd, "-o", "/dev/null", "--width", "1920", "--height", "1080", "-n"],
            check=True,
            capture_output=True,
            timeout=10
        )
        return True, None
    except subprocess.CalledProcessError as e:
        stderr_text = (e.stderr or b"").decode("utf-8", errors="replace").strip()
        stdout_text = (e.stdout or b"").decode("utf-8", errors="replace").strip()
        details = stderr_text or stdout_text or str(e)
        return False, details
    except subprocess.TimeoutExpired:
        return False, "Camera capture timed out after 10 seconds"

if __name__ == "__main__":
    print("=" * 70)
    print("CAMERA SENSOR TEST")
    print("=" * 70)
    print(f"Using camera command: {get_camera_command()}")
    print("Testing camera connection every 2 seconds...")
    print("Press Ctrl+C to stop.\n")
    
    test_count = 0
    success_count = 0
    last_error = None
    
    try:
        while True:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            test_count += 1
            
            is_working, error_details = test_camera()
            
            if is_working:
                success_count += 1
                if last_error is not None:
                    print(f"[{test_count}] {timestamp} | Camera: OK (recovered)")
                else:
                    print(f"[{test_count}] {timestamp} | Camera: OK")
                last_error = None
            else:
                print(f"[{test_count}] {timestamp} | Camera: FAILED - Could not capture test image")
                if last_error is None:
                    # print detailed diagnostics only once
                    print(f"    Details: {error_details}")
                    last_error = error_details
            
            time.sleep(2)
    
    except KeyboardInterrupt:
        print("\n" + "=" * 70)
        print(f"Test stopped. {success_count}/{test_count} successful tests.")
        print("=" * 70)
