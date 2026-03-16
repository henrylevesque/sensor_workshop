import time
import os
from datetime import datetime
import subprocess
import shutil

# This script captures images from a camera connected to a Raspberry Pi.
# Images are collected at set intervals for a set duration and saved to a folder.
# Images are saved immediately after each capture, so no data is lost if power fails.
# Text that follows the '#' symbol is a comment and is not executed as part of the code.

# INSTALLATION INSTRUCTIONS (run on Raspberry Pi):
# Step 1: Update system packages
#   sudo apt update
# Step 2: Install camera apps (choose one based on your OS)
#   sudo apt install -y rpicam-apps    # Raspberry Pi OS Bookworm/newer
#   sudo apt install -y libcamera-apps # Raspberry Pi OS Bullseye/older

# Camera support: Raspberry Pi Camera Module or compatible CSI camera
# Images are stored as JPEG files with timestamps as filenames

def get_camera_command():
    """Return available still-image camera command for this OS."""
    for cmd in ("rpicam-still", "libcamera-still"):
        if shutil.which(cmd) is not None:
            return cmd

    raise EnvironmentError(
        "No camera capture command found. Install one of:\n"
        "  sudo apt update\n"
        "  sudo apt install -y rpicam-apps   # Raspberry Pi OS Bookworm/newer\n"
        "  sudo apt install -y libcamera-apps # Raspberry Pi OS Bullseye/older"
    )


CAMERA_CMD = get_camera_command()

# Function to capture an image using libcamera
def capture_image(image_path):
    """Capture a single image and save it to the specified path"""
    try:
        subprocess.run(
            [CAMERA_CMD, "-o", image_path, "--width", "1920", "--height", "1080", "-n"],
            check=True,
            capture_output=True,
            timeout=30
        )
        return True, None
    except subprocess.CalledProcessError as e:
        stderr_text = (e.stderr or b"").decode("utf-8", errors="replace").strip()
        stdout_text = (e.stdout or b"").decode("utf-8", errors="replace").strip()
        details = stderr_text or stdout_text or str(e)
        print(f"Error capturing image: {details}")
        return False, details
    except subprocess.TimeoutExpired:
        print("Image capture timed out")
        return False, "Image capture timed out"

# Function to collect images for a specified duration and interval
def collect_images(duration_minutes, interval_seconds, folder_path="captured_images"):
    """
    Collect images at regular intervals for a specified duration.
    
    Args:
        duration_minutes: How long to collect images (in minutes)
        interval_seconds: Interval between captures (in seconds)
        folder_path: Directory to save images in
    """
    start_time = time.time()
    duration_seconds = duration_minutes * 60
    capture_count = 0
    success_count = 0
    
    # Create the folder if it doesn't exist
    os.makedirs(folder_path, exist_ok=True)
    
    print(f"Using camera command: {CAMERA_CMD}")
    print(f"Starting image capture for {duration_minutes} minutes (capturing every {interval_seconds} seconds)...")
    print(f"Images will be saved to: {folder_path}")
    print("-" * 70)

    last_error = None
    try:
        while time.time() - start_time < duration_seconds:
            # Get current timestamp for the filename
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            
            # Create full image path
            image_name = f"{folder_path}/image_{timestamp}.jpg"
            
            # Capture image
            capture_count += 1
            capture_ok, error_details = capture_image(image_name)
            if capture_ok:
                success_count += 1
                if last_error is not None:
                    print(f"[{capture_count}] {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Image saved: {image_name} (recovered)")
                else:
                    print(f"[{capture_count}] {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Image saved: {image_name}")
                last_error = None
            else:
                print(f"[{capture_count}] {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Image capture failed, will retry next interval")
                if last_error is None:
                    print(f"    Details: {error_details}")
                    last_error = error_details
            
            # Wait for the next interval
            remaining_time = duration_seconds - (time.time() - start_time)
            if remaining_time > 0:
                time.sleep(min(interval_seconds, remaining_time))

    except KeyboardInterrupt:
        print("\n" + "-" * 70)
        print(f"Image capture stopped.")
    
    print("-" * 70)
    print(f"Capture complete. {success_count}/{capture_count} successful captures.")
    print(f"Images saved to: {folder_path}")

# Example usage
if __name__ == "__main__":
    duration_minutes = 5  # Set the duration in minutes here
    interval_seconds = 10  # Set the interval in seconds here
    folder_path = "captured_images"  # Set the folder path here
    collect_images(duration_minutes, interval_seconds, folder_path)
