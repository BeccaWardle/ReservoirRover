#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import ADS1263
# import RPi.GPIO as GPIO
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# matplotlib setup
fig = plt.figure()
# fig.canvas.set_window_title("IR Readings")
polar = plt.subplot(polar=True)
# polar.autoscale_view(True, True, True)
# polar.set_rmax(3)
# polar.grid(True)


def animate(waste):
    ADC_Values = ADC.ADS1263_GetAll()    # get ADC1 value
    volts = []
    rads = []
    sensors_n = 6
    rads = [2.3562, 3.1416, 3.9270, 4.7124, 5.4978, 0.0, 0.7854]
    # rads = [3.9270, 3.1416, 2.3562, 1.5707, 0.7854, 0.0, 5.4978]
    for i in range(sensors_n + 1):
        print(f"ADC1 IN{i} = {(REF*2 - ADC_Values[i] * REF / 0x7fffffff)} : {rads[i]}")
        volts.append(round(ADC_Values[i], 5))
        # * REF / 0x7fffffff)
        # print(f"ADC1 {i} = {(ADC_Values[i])} : {rads[i]}")   # 32bit 0x80000000
    polar.clear()
    polar.scatter(rads, volts)


REF = 5.08          # Modify according to actual voltage
# external AVDD and AVSS(Default), or internal 2.5V

try:
    ADC = ADS1263.ADS1263()
    if (ADC.ADS1263_init() == -1):
        print("Init error")
        exit()
    while(True):
        anim = animation.FuncAnimation(fig, animate, interval=1)
        plt.show()
    # animate()

    ADC.ADS1263_Exit()

except IOError as e:
    print(e)

except KeyboardInterrupt:
    print("ctrl + c:")
    print("Program end")
    ADC.ADS1263_Exit()
    exit()

