import RPi.GPIO as GPIO
import subprocess
import os
import time
from datetime import datetime
# Setup your capacitive touch sensor pin
touchSensorPin = 21
audio_folder = "./New_Audios/"
def setup():
    GPIO.setmode(GPIO.BCM)  # Use BCM numbering
    GPIO.setup(touchSensorPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Setup touch sensor pin
def record_audio(filename, duration=10):
    # Command to record audio from default USB mic to specified file for a duration in seconds
    command = f"arecord -d {duration} -f S16_LE -q {filename}.wav"
    subprocess.run(command, shell=True)
def play_audio(filename, volume_percent=100):
    # Adjust the system volume
    set_volume_command = f"amixer set Master {volume_percent}%"
    subprocess.run(set_volume_command, shell=True)
    # Command to play audio file
    play_command = f"aplay {filename}.wav"
    subprocess.run(play_command, shell=True)
def loop():
    print("System ready. Touch the sensor to record and play audio.")
    while True:
        if GPIO.input(touchSensorPin) == GPIO.HIGH:
            current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")  # Get current date and time
            audio_file = os.path.join(audio_folder, f"recorded_audio_{current_time}")
            print("Touch detected! Recording and playing back audio...")
            record_audio(audio_file)
            play_audio(audio_file)
            while GPIO.input(touchSensorPin) == GPIO.HIGH:
                # Wait for the user to release the touch sensor
                pass
if __name__ == '__main__':
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        print("Exiting program")
        GPIO.cleanup()  # Clean up GPIO on CTRL+C exit
