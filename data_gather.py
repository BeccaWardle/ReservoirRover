#!/usr/bin/env python3
import os
import sys
from datetime import datetime as dt

import ydlidar

from IR import ADS1263

# Create directory for files
FILE = "data/" + str(sys.argv[1])

if not os.path.isdir(FILE):
    os.mkdir(FILE)

os.chdir(FILE)


# number of IR sensors on device
SENSORS = 4
# voltage the IR sensors receive
IR_VOLTAGE = 5.08


## Configure LIDAR
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

LASER_init = LASER.initialize()
for i in range(20000):
    # Files named based on time of data collection
    F_NAME = str(dt.now()).replace(":", "-").split(".")[0].replace(" ", "_") \
        + "." + str(dt.now()).split(".")[1][:2]

    with open(F_NAME, "w") as file:

        # Lidar recording
        if LASER_init:
            laser_on = LASER.turnOn()
            if laser_on:
                single_scan = LASER.doProcessSimple(LASER_SCAN)
                if single_scan:
                    for point in LASER_SCAN.points:
                        file.write(f"{point.angle}, {point.range}, {point.intensity}\n")

        file.write("\n")

        # IR recording
        ADC = ADS1263.ADS1263()
        if ADC.ADS1263_init() == -1:
            print("IR intilisation error")
            sys.exit()
        ADC_vales = ADC.ADS1263_GetAll()
        volts = []
        # The angle of the IR sensors added to this but need to be added manually
        rads = []
        file.write(f"Voltage Ref: {IR_VOLTAGE}\n")
        for n in range(SENSORS + 1):
            file.write(f"{ADC_vales[n]}, ")
        file.write("\n")

# Turn off IO
ADC.ADS1263_Exit()
LASER.turnOff()
LASER.disconnecting()
