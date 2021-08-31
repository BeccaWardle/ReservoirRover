#!/usr/bin/env python3
import os
import ydlidar
from IR import ADS1263
import sys
from datetime import datetime as dt
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
                l_angle.append(point.angle)
                l_range.append(point.range)

    # IR Data
    ADC_vales = ADC.ADS1263_GetAll()
    IR_volts = []
    IR_rads = [2.3562, 3.1416, 3.9270, 4.7124, 5.4978, 0.0, 0.7854]
    for i in range(sensors + 1):
        # file.write(round(ADC_vales[i], 5))
        IR_volts.append(IR_voltage * 2 - ADC_vales[i] * IR_voltage / 0x7fffffff)

    lidar_polar.clear()
    lidar_polar.scatter(l_angle, l_range, cmap="hsv", alpha=0.95)
    lidar_polar.scatter(IR_rads, IR_volts, c="green", alpha=0.95)


# Configure plot
fig = plt.figure()

lidar_polar = plt.subplot(polar=True)
lidar_polar.autoscale_view(True,True,True)
lidar_polar.set_rmax(32)
lidar_polar.grid(True)
# number of IR sensors on device
sensors = 7
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
    anim = animation.FuncAnimation(fig, animator, interval= 5)
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
