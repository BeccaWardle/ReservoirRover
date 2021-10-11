#!/usr/bin/env python3

"""
Creates a matplotlib annimation plotting the lidar and IR sensors onto a polar graph
"""

from math import pi
from sys import exit as sys_exit

import matplotlib.pyplot as plt
import ydlidar
from matplotlib import animation

from IR import ADS1263


def animator(num):
    """
    Annimator funtion for maplotlib.annimation
    Collects the Lidar and IR data and adds them as plots to a polar graph
    """
    # Lidar data
    l_angle = []
    l_range = []
    laser_on = LASER.turnOn()
    if laser_on:
        laser_scan = LASER.doProcessSimple(LASER_SCAN)
        if laser_scan:
            for point in LASER_SCAN.points:
                l_angle.append(point.angle)
                l_range.append(point.range)

    # IR Data
    ir_distances = []
    ir_rads = [0.0 ,pi / 2, pi, (3 * pi) / 2]

    adc_vales = ADC.ADS1263_GetAll()

    for i in range(SENSORS):
        voltage = adc_vales[i] * IR_REF_VOLTAGE / 0x7fffffff

        ir_dist = 29.988 * pow(voltage, -1.173) / 100
        ir_distances.append(ir_dist)

    lidar_polar.clear()
    lidar_polar.set_theta_direction(-1)
    lidar_polar.fill_between(l_angle, l_range, color="green", alpha=0.5)
    lidar_polar.scatter(l_angle, l_range, color="yellow", alpha=0.5)
    lidar_polar.scatter(ir_rads, ir_distances, c="red", alpha=0.95)
    print(f"\033[{SENSORS + 2}A")


# Configure plot
fig = plt.figure()

lidar_polar = plt.subplot(polar=True)
lidar_polar.autoscale_view(True,True,True)
lidar_polar.set_rmax(32)
lidar_polar.grid(True)

# number of IR sensors on device
SENSORS = 4
# voltage the IR sensors receive
IR_REF_VOLTAGE = 5.08


## Configure LIDAR access
RMAX = 32.0

PORTS = ydlidar.lidarPortList()
PORT = "/dev/ydlidar"

for key, value in PORTS.items():
    print(value)
    PORT = value

LASER = ydlidar.CYdLidar()
LASER.setlidaropt(ydlidar.LidarPropSerialPort, PORT)
LASER.setlidaropt(ydlidar.LidarPropSerialBaudrate, 128000)
LASER.setlidaropt(ydlidar.LidarPropLidarType, ydlidar.TYPE_TRIANGLE)
LASER.setlidaropt(ydlidar.LidarPropDeviceType, ydlidar.YDLIDAR_TYPE_SERIAL)
LASER.setlidaropt(ydlidar.LidarPropScanFrequency, 10.0)
LASER.setlidaropt(ydlidar.LidarPropSampleRate, 9)
LASER.setlidaropt(ydlidar.LidarPropSingleChannel, False)

LASER_SCAN = ydlidar.LaserScan()

LASER_INIT = LASER_SCAN.initialize()


try:
    # IR recording
    ADC = ADS1263.ADS1263()
    if ADC.ADS1263_init() == -1:
        print("IR Init error")
        sys_exit()
    anim = animation.FuncAnimation(fig, animator, interval= 1)
    plt.show()

except KeyboardInterrupt:
    print("Quiting")
    # Turn off IO
    ADC.ADS1263_Exit()
    LASER.turnOff()
    LASER.disconnecting()
    plt.close()
    sys_exit()

ADC.ADS1263_Exit()
LASER.turnOff()
LASER.disconnecting()
plt.close()
