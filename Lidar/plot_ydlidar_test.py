#!/usr/bin/env python3
import ydlidar
# import time
# import sys
# from matplotlib.patches import Arc
import matplotlib.pyplot as plt
import matplotlib.animation as animation
# import numpy as np

def animate(num):
    r = laser.doProcessSimple(scan);
    if r:
        angle = []
        ran = []
        intensity = []
        for point in scan.points:
            if point.range != 0:
                angle.append(point.angle);
                ran.append(point.range);
                intensity.append(point.intensity);
        lidar_polar.clear()
        lidar_polar.set_theta_direction(-1)
        lidar_polar.scatter(angle, ran, c=intensity, cmap='hsv', alpha=0.95)



RMAX = 32.0


fig = plt.figure()
# fig.canvas.set_window_title('YDLidar LIDAR Monitor')

lidar_polar = plt.subplot(projection="polar")
lidar_polar.set_theta_direction(-1)
lidar_polar.autoscale_view(True,True,True)
lidar_polar.set_rmax(RMAX)
lidar_polar.grid(True)

ports = ydlidar.lidarPortList();
port = "/dev/ydlidar";

for key, value in ports.items():
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
    if ret:
        print("Turning on")
        ret = laser.turnOn();
        if ret:
            ani = animation.FuncAnimation(fig, animate, interval=5)
            plt.show()
        else:
            print("Failed to turn on")
        laser.turnOff();

except KeyboardInterrupt:
    laser.disconnecting();
    plt.close();
laser.disconnecting()
plt.close()
