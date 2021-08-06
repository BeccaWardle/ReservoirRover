#!/usr/bin/python
# -*- coding:utf-8 -*-

import ADS1263
import RPi.GPIO as GPIO
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
    for i in range(sensors_n + 1):
        # if(ADC_Value[i]>>31 == 1):
            # print("ADC1 IN%d = -%lf" %(i, (REF*2 - ADC_Value[i] * REF / 0x80000000)))
        volts.append(round(ADC_Values[i], 5))
        rads.append(round(3.14159265359/sensors_n * i, 5))
        print(f"ADC1 {i} = {(ADC_Values[i] * REF / 0x7fffffff)} : {rads[i]}")   # 32bit
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
        anim = animation.FuncAnimation(fig, animate, interval=4)
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

