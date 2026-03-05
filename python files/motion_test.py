from gpiozero import MotionSensor
from signal import pause

# PIR connected to GPIO 23
pir = MotionSensor(23)

print("=" * 70)
print("PIR MOTION SENSOR TEST")
print("=" * 70)
print("Sensor is warming up (allowing it to settle)...")
pir.wait_for_no_motion() # Allow sensor to settle
print("Sensor ready. Waiting for motion...")
print("Press Ctrl+C to stop.\n")

def motion_detected():
    print(">>> MOTION DETECTED!")

def motion_stopped():
    print(">>> Motion stopped.")

# Call functions when motion is detected
pir.when_motion = motion_detected
pir.when_no_motion = motion_stopped

pause()
