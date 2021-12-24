import RPi.GPIO as GPIO
import time

# GPIO which are connected to the LEDs
red_gpio = 4
green_gpio = 5
blue_gpio = 6

# Set GPIO low to turn on LED in this config
# May reverse this if we
on = GPIO.LOW
off = GPIO.HIGH


# Setup the GPIO
def setup_led_gpio():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(red_gpio, GPIO.OUT)
    GPIO.setup(blue_gpio, GPIO.OUT)
    GPIO.setup(green_gpio, GPIO.OUT)

    GPIO.output(red_gpio, off)
    GPIO.output(blue_gpio, off)
    GPIO.output(green_gpio, off)


def all_off():
    GPIO.output(red_gpio, off)
    GPIO.output(blue_gpio, off)
    GPIO.output(green_gpio, off)


def red():
    GPIO.output(red_gpio, on)
    GPIO.output(blue_gpio, off)
    GPIO.output(green_gpio, off)


def orange():
    GPIO.output(red_gpio, on)
    GPIO.output(blue_gpio, off)
    GPIO.output(green_gpio, on)


def green():
    GPIO.output(red_gpio, off)
    GPIO.output(blue_gpio, off)
    GPIO.output(green_gpio, on)


def blue():
    GPIO.output(red_gpio, off)
    GPIO.output(blue_gpio, on)
    GPIO.output(green_gpio, off)


# Loop this if you want it to blink
def blink_red():
    GPIO.output(red_gpio, on)
    GPIO.output(blue_gpio, off)
    GPIO.output(green_gpio, off)
    time.sleep(0.5)
    GPIO.output(red_gpio, off)
    time.sleep(0.5)


setup_led_gpio()

if __name__ == "__main__":
    print('Looping color test...')
    while True:
        all_off()
        time.sleep(1)
        red()
        time.sleep(1)
        green()
        time.sleep(1)
        blue()
        time.sleep(1)
        orange()
        time.sleep(1)
        for i in range(0, 3):
            blink_red()
        time.sleep(2)