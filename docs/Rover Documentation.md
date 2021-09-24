# Rover Documentation

This is the documentation for the York University Rover research platform (my name not theirs). It is designed to be an expandable platform for robotics reaserch.
It includes:

- Raspberry Pi [TODO: check]
- Xilinx Digilent Zybo Z7
- YDLidar X4
- High Precision AD HAT
- 5x IR Sensors
  - 3x Sharp 2Y0A21 YK0F (10-80cm)
  - 2x Sharp 2Y0A41 SK0F (4-30cm)
- Sabertooth 2X12
- 4x DC motors
- 4x motor encoders
- 2x 5 Volt regulators

The code I have written is on the Raspberry Pi and is in Python 3. One program records data from the IR and Lidar to the Pi's SD card for later processing, the other program plots the Lidar and IR data in real time onto a polar graph using Matplotlib.

## Hardware

My project was focused on using the Lidar and IR sensors for positional processing. This left several pieces of hardware unused.
I disconnected the FPGA chip from power but left most of its connections to the Pi as these were set up by a previous student. The motor encoders have also been left completely detatched.

![Functional Diagram](./Function%20Diagram.png)

As shown in the diagram a (3 cell) lipo battery was used to power the sytem, this was due to issues with the provided UPS. Both the Pi and LIDAR are powered from this via USB cables with stripped ends.

### Raspberry Pi

The Raspberry Pi is a model 3B running Raspbian.

The Pi has an HAT which allows it to read the IR sensors. Most of the GPIO pins on this HAT are connected to the FPGA and are a hold over from an earlier project.

The original FPGA connections are show below

<img alt="FPGA Connection Left Side" src="./FPGA%20Connections%20Left.jpg" width="350"/>
<img alt="FPGA Connection Right Side" src="./FPGA%20Connections%20Right.jpg" width="350"/>

### LIDAR

YDLIDAR X4: <https://www.ydlidar.com/Public/upload/files/2021-08-20/YDLIDAR%20X4%20Data%20sheet%20V2.0.pdf>

Power provided by seperate 5V regulator to the Pi and IR sensors. This is to avoid voltage spikes that prevented the Lidar motor from spinning up when it's turned on.

The LIDAR is connected to the Pi via a micro USB cable.

### IR Sensors

[TODO: Create diagram of IR sensors (where on rover)]

Voltages read through [High Precision AD HAT](https://www.waveshare.com/wiki/High-Precision_AD_HAT)
Datasheet: <https://www.waveshare.com/w/upload/2/2a/Ads1262.pdf>

Image Sharp:
<https://global.sharp/products/device/lineup/data/pdf/datasheet/gp2y0a21yk_e.pdf>
<https://www.pololu.com/file/0J713/GP2Y0A41SK0F.pdf>

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
