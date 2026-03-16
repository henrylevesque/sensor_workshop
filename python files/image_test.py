import time
from datetime import datetime
import subprocess
import shutil

# This is a quick test script to verify the camera is working.
# Press Ctrl+C to stop.

# Camera support: Raspberry Pi Camera Module or compatible CSI camera
# Requires libcamera to be installed on the system

def test_camera():
    """Test if camera is working by capturing a test image"""
    if shutil.which("libcamera-still") is None:
        raise RuntimeError(
            "libcamera-still command not found. Install with:\n"
            "  sudo apt update\n"
            "  sudo apt install -y camera-stack libcamera-apps"
        )
    
    try:
        # Capture a test image to /dev/null (doesn't save it)
        subprocess.run(
            ["libcamera-still", "-o", "/dev/null", "--width", "1920", "--height", "1080", "-n"],
            check=True,
            capture_output=True,
            timeout=10
        )
        return True
    except subprocess.CalledProcessError as e:
        return False
    except subprocess.TimeoutExpired:
        return False

if __name__ == "__main__":
    print("=" * 70)
    print("CAMERA SENSOR TEST")
    print("=" * 70)
    print("Testing camera connection every 2 seconds...")
    print("Press Ctrl+C to stop.\n")
    
    test_count = 0
    success_count = 0
    
    try:
        while True:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            test_count += 1
            
            is_working = test_camera()
            
            if is_working:
                success_count += 1
                print(f"[{test_count}] {timestamp} | Camera: OK")
            else:
                print(f"[{test_count}] {timestamp} | Camera: FAILED - Could not capture test image")
            
            time.sleep(2)
    
    except KeyboardInterrupt:
        print("\n" + "=" * 70)
        print(f"Test stopped. {success_count}/{test_count} successful tests.")
        print("=" * 70)
