#!/usr/bin/python
# -*- coding:utf-8 -*-


import time
import IR.ADS1263 as ADS1263
import RPi.GPIO as GPIO

REF = 5.8# Modify according to actual voltage
print(f"REF= {REF}")
# external AVDD and AVSS(Default), or internal 2.5V
TEST_ADC = True        # ADC Test part
TEST_RTD = False        # RTD Test part

vals = []

try:
    ADC = ADS1263.ADS1263()
    if (ADC.ADS1263_init() == -1):
        exit()

    # ADC.ADS1263_DAC_Test(1, 1)      # Open IN6
    # ADC.ADS1263_DAC_Test(0, 1)      # Open IN7
    while(1):
        if(TEST_ADC):       # ADC Test
            ADC_Value = ADC.ADS1263_GetAll()    # get ADC1 value
            for i in range(1):
                vals.append(ADC_Value[i])
                if(ADC_Value[i] >> 31 == 1):
                    print(f"ADC1 IN{i}: {hex(ADC_Value[i])} => {-1 * (REF*2 - ADC_Value[i] * REF / 0x80000000)}")
                else:
                    print(f"ADC1 IN{i}: {hex(ADC_Value[i])} => {REF*2 - ADC_Value[i] * REF / 0x7fffffff}")
                    print(f"max val: {max(vals):>5} min val: {min(vals)}")

                    # print("ADC1 IN%d = %lf" %(i, (ADC_Value[i] * REF / 0x7fffffff)))   # 32bit

            print("\33[4A")

        elif(TEST_RTD):     # RTD Test
            ADC_Value = ADC.ADS1263_RTD_Test()
            RES = ADC_Value / 2147483647.0 * 2.0 *2000.0       #2000.0 -- 2000R, 2.0 -- 2*i
            print("RES is %lf"%RES)
            TEMP = (RES/100.0 - 1.0) / 0.00385      #0.00385 -- pt100
            print("TEMP is %lf"%TEMP)
            print("\33[4A")

except IOError as e:
    print(e)

except KeyboardInterrupt:
    print("\33[3B")
    vals.sort()
    print(f"range: {hex(vals[0])} - {hex(vals[-1])} = {vals[0]} - {vals[-1]}")
    print(f"mean: {hex(int(sum(vals)/len(vals)))} = {int(sum(vals)/len(vals))}")
    print(f"median: {hex(vals[int(len(vals)/2)])} = {vals[int(len(vals)/2)]}")


    print("ctrl + c:")
    print("Program end")
    ADC.ADS1263_Exit()
    exit()

