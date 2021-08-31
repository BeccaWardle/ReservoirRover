#!/usr/bin/env python3
import os
import ydlidar
import IR.ADS1263
import sys
from datetime import datetime as dt


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

# Create directory for files
file = "data/" + str(sys.argv[1])

if not os.path.isdir(file):
    os.mkdir(file)

os.chdir(file)

scan = ydlidar.LaserScan()

ret = laser.initialize();
for i in range(20000):
    # TODO: Rename output to comply with Windows file system
    fname = str(dt.now())

    with open(fname, "w") as file:

        # Lidar recording
        if ret:
            ret = laser.turnOn();
            if ret:
                r = laser.doProcessSimple(scan);
                if r:
                    for point in scan.points:
                        file.write(f"{point.angle}, {point.range}, {point.intensity}\n")

        file.write("\n")

        # IR recording
        ADC = ADS1263.ADS1263()
        if (ADC.ADS1263_init() == -1):
            print("Init error")
            exit()
        ADC_vales = ADC.ADS1263_GetAll()
        volts = []
        rads = []
        for i in range(sensors + 1):
            file.write(round(ADC_vales[i], 5))


laser.turnOff();

laser.disconnecting();
plt.close();
