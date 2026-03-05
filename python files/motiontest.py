from gpiozero import MotionSensor
from signal import pause

# PIR connected to GPIO 23
pir = MotionSensor(23)

print("PIR Sensor is warming up...")
pir.wait_for_no_motion() # Allow sensor to settle
print("Sensor ready.")

def motion_detected():
    print("Motion Detected!")

def motion_stopped():
    print("Motion Stopped.")

# Call functions when motion is detected
pir.when_motion = motion_detected
pir.when_no_motion = motion_stopped

pause()
