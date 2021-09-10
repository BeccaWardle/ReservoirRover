#!/usr/bin/env python3

import RPi.GPIO as GPIO
from time import sleep

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
pin1 = 12
pin2 = 33

GPIO.setup(pin1, GPIO.OUT)
GPIO.setup(pin2, GPIO.OUT)
pin1_pwm = GPIO.PWM(pin1, 1000)
pin2_pwm = GPIO.PWM(pin2, 1000)

pin1_pwm.start(0)
pin2_pwm.start(0)

try:
    while True:
        print("Stay")
        pin1_pwm.ChangeDutyCycle(50)
        pin2_pwm.ChangeDutyCycle(50)
        sleep(1.5)
        print("Forward")
        pin1_pwm.ChangeDutyCycle(100)
        pin2_pwm.ChangeDutyCycle(100)
        sleep(2)
        print("Backward")
        pin1_pwm.ChangeDutyCycle(0)
        pin2_pwm.ChangeDutyCycle(0)
        sleep(2.1)
        print("Turn")
        pin1_pwm.ChangeDutyCycle(100)
        pin2_pwm.ChangeDutyCycle(0)
        sleep(2)
        print("Turn")
        pin1_pwm.ChangeDutyCycle(0)
        pin2_pwm.ChangeDutyCycle(100)
        sleep(2)
        print("Stop")
        pin1_pwm.ChangeDutyCycle(50)
        pin2_pwm.ChangeDutyCycle(50)
        sleep(2)


except KeyboardInterrupt:
    pin1_pwm.stop()
    pin2_pwm.stop()
