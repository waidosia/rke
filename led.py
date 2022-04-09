import RPi.GPIO as GPIO
import time

def led():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18, GPIO.OUT)
    GPIO.output(18, GPIO.HIGH)
    time.sleep(3.0)
    GPIO.output(18, GPIO.LOW)
    GPIO.cleanup()


if __name__ == '__main__':
    led()