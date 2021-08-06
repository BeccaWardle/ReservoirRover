#!/usr/bin/env python3
import os
import ydlidar
import sys
from datetime import datetime as dt



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

# Create directory for files
file = "Output/" + str(sys.argv[1])

if not os.path.isdir(file):
    os.mkdir(file)

os.chdir(file)

scan = ydlidar.LaserScan()

ret = laser.initialize();
for i in range(20000):
    print(str(dt.now()))
    fname = str(dt.now())

    with open(fname, "w") as file:
        if ret:
            ret = laser.turnOn();
            if ret:
                r = laser.doProcessSimple(scan);
                if r:
                    for point in scan.points:
                        file.write(f"{point.angle}, {point.range}, {point.intensity}\n")

laser.turnOff();

laser.disconnecting();
plt.close();
