# Rover Documentation

This is the documentation for the York University Rover research platform. It is designed to be an expandable platform for robotics research.
It includes:

- [Raspberry Pi 3B+](#raspberry-pi)
- Xilinx Digilent Zybo Z7
- [YDLidar X4](#lidar)
- High Precision AD HAT
- 5x [IR Sensors](#ir-sensors)
  - 3x Sharp GP2Y0A21YK0F (10-80cm)
  - 2x Sharp GP2Y0A41SK0F (4-30cm)
- [Sabertooth 2x12](#motor-driver)
- 4x DC motors
- 4x motor encoders
- 2x 5 Volt regulators

The code is in Python3 on the Raspberry Pi. <br>
One program to record data from the IR and Lidar to the Pi's SD card, another to plot the Lidar and IR data in real time

## Hardware

The focus of my project was focused on using the Lidar and IR sensors for positional processing. <br>
This left several pieces of hardware unused:
- The FPGA chip, which I disconnected from power
- Pi to FPGA connections (left all but pin 12 and 33 connected)
- Motor encoders (completely detatched)

<br>

### System Overview

![Functional Diagram](./Function%20Diagram.png)

As shown in the diagram a (3 cell) lipo battery was used to power the sytem, this was due to issues with the provided UPS. Both the Pi and LIDAR are powered from this via USB cables with stripped ends.

To avoid issues powering both the Lidar and Pi simultanouesly they each have their own a voltage regulator. <br>
One of the regulators (lidar) is connected via the breadboard the other (pi and IR) is connected via red and blue GPIO header cables.

<img alt="Regulators" src="./Regulator.jpg"/>


### Raspberry Pi

The Raspberry Pi is a model 3B running Raspbian.

The Pi has an HAT which allows it to read the IR sensors.
Most of the GPIO pins on this HAT are connected to the FPGA and are a hold over from an earlier project.

The original FPGA connections are show below

<img alt="FPGA Connection Left Side" src="./FPGA%20Connections%20Left.jpg" width="350"/>
<img alt="FPGA Connection Right Side" src="./FPGA%20Connections%20Right.jpg" width="350"/>

The Pi connected via ground to a common ground shared by all the components.

### IR Sensors

The IR sensors are supplied 5V by the same voltage regulator as the Pi via a power rail on the breadboard.

<img alt="IR Power Rail" src="./Power%20Bus.jpg">

There are 2 different IR sensors on the vehicle. 
- [GP2Y0A21YK0F](https://global.sharp/products/device/lineup/data/pdf/datasheet/gp2y0a21yk_e.pdf) (aka 2Y0A21)
- [GP2Y0A41SK0F](https://global.sharp/products/device/lineup/data/pdf/datasheet/gp2y0a41sk_e.pdf) (aka 0A41SK) 

Whilst most can be identified by the serial number on their cases some have suffered damage so have been labelled.  

2Y0A21 have a range of 10-80cm <br>
0A41SK have a range of  4-30cm

The layout of the IR sensors:
<img alt="IR layout" src="./Rover.png">

The IR sensors output a voltage which is read through a [High Precision AD HAT](https://www.waveshare.com/wiki/High-Precision_AD_HAT) ([Datasheet](https://www.waveshare.com/w/upload/2/2a/Ads1262.pdf))

### LIDAR

The LIDAR is a [YDLIDAR X4](https://www.ydlidar.com/Public/upload/files/2021-08-20/YDLIDAR%20X4%20Data%20sheet%20V2.0.pdf)

Power is provided by seperate 5V regulator to the Pi and IR sensors. This is to avoid voltage spikes that prevented the Lidar motor from spinning up when it's turned on.

The regulator and lidar are both connected via the breadboards' lowest power rail. 

The LIDAR is connected to the Pi via a micro USB cable. 


### Motor Driver

[TODO: get settings of the motor driver]
PWM mode, tank based
Not set correctly

80 is stationary, 100 is forward
Faster backwards than forwards

<https://www.dimensionengineering.com/datasheets/Sabertooth2x12.pdf>

## Software

The software for this project was written in Python 3

I made use of <https://github.com/YDLIDAR/YDLidar-SDK> to control the LIDAR

## Plotting Code

### Recording Code
