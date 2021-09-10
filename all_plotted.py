#!/usr/bin/env python3
import os
import ydlidar
from IR import ADS1263
import sys
from datetime import datetime as dt
from math import pi
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def animator(num):
    # Lidar data
    l_angle = []
    l_range = []
    ret = laser.turnOn();
    if ret:
        r = laser.doProcessSimple(scan);
        if r:
            for point in scan.points:
                # if int(point.range) == 0:
                    # continue
                # if point.range < 4:
                l_angle.append(point.angle)
                l_range.append(point.range)
                # else:
                    # l_angle.append(point.angle)
                    # l_range.append(4)

    # IR Data
    ADC_vales = ADC.ADS1263_GetAll()
    IR_volts = []
    IR_rads = [0.0 ,pi / 2, pi, (3 * pi) / 2]
    for i in range(sensors):
        # file.write(round(ADC_vales[i], 5))
        tmp_volt = ADC_vales[i] * IR_voltage / 0x7fffffff
        print(f"sensor[{i}]: {hex(ADC_vales[i]):>5} {tmp_volt:>5} {29.988 * pow(tmp_volt, -1.173)}")
        # if tmp_volt < 0.25:

            # tmp_volt = 0
            # tmp_dist = 0
        # else:
        tmp_dist = 29.988 * pow(tmp_volt, -1.173) / 100
        if tmp_dist > 0.7:
            tmp_dist = 0

        IR_volts.append(tmp_dist)

    # print(IR_volts)
    # print(IR_rads)

    lidar_polar.clear()
    lidar_polar.set_theta_direction(-1)
    lidar_polar.fill_between(l_angle, l_range, color="green", alpha=0.5)
    lidar_polar.scatter(l_angle, l_range, color="yellow", alpha=0.5)
    lidar_polar.scatter(IR_rads, IR_volts, c="red", alpha=0.95)
    print(f"\033[{sensors + 2}A")


# Configure plot
fig = plt.figure()

lidar_polar = plt.subplot(polar=True)
lidar_polar.autoscale_view(True,True,True)
lidar_polar.set_rmax(32)
lidar_polar.grid(True)
# number of IR sensors on device
sensors = 4
# voltage the IR sensors receive
IR_voltage = 5.08


## Sort out LIDAR access
RMAX = 32.0

ports = ydlidar.lidarPortList();
port = "/dev/ydlidar";

for key, value in ports.items():
    print(value)
    port = value;

laser = ydlidar.CYdLidar();
laser.setlidaropt(ydlidar.LidarPropSerialPort, port);
laser.setlidaropt(ydlidar.LidarPropSerialBaudrate, 128000)
laser.setlidaropt(ydlidar.LidarPropLidarType, ydlidar.TYPE_TRIANGLE);
laser.setlidaropt(ydlidar.LidarPropDeviceType, ydlidar.YDLIDAR_TYPE_SERIAL);
laser.setlidaropt(ydlidar.LidarPropScanFrequency, 10.0);
laser.setlidaropt(ydlidar.LidarPropSampleRate, 9);
laser.setlidaropt(ydlidar.LidarPropSingleChannel, False);

scan = ydlidar.LaserScan()

ret = laser.initialize();


try:
    # IR recording
    ADC = ADS1263.ADS1263()
    if (ADC.ADS1263_init() == -1):
        print("IR Init error")
        exit()
    anim = animation.FuncAnimation(fig, animator, interval= 1)
    plt.show()

except KeyboardInterrupt:
    print("Quiting")
    ADC.ADS1263_Exit()
    laser.turnOff();
    laser.disconnecting();
    plt.close();
    exit()

ADC.ADS1263_Exit()
laser.turnOff();
laser.disconnecting();
plt.close();
