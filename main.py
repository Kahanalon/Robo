from robomaster import robot
import PySimpleGUI as sg
import time

ep_robot = robot.Robot()

connected = ep_robot.initialize(conn_type="ap")

ep_chassis = ep_robot.chassis
ep_version = ep_robot.get_version()
print("Robot Version: {0}".format(ep_version))


if connected:
    print('connected')

else:
    print("ERROR - failed to connect")


def get_nway_dis(n):
    dist_array = []
    for i in range(n):
        dist_array.append(average_dis(5))  # 5 distance samples
        ep_chassis.move(0, 0, 360 / n, xy_speed=1, z_speed=30).wait_for_completed()
    return dist_array

def dis(x):
    y = x

def average_dis(num_of_readings):
    n = num_of_readings
    total_dis = 0
    dif_dist = []
    while n > 0:
        ep_robot.sensor.sub_distance(freq=1, callback=lambda x: dif_dist.append(x))
        print(dif_dist)
        # ep_robot.unsub_distance( )
        #total_dis += cur_dis
        n -=1
    # ep_robot.sensor.unsub_distance()
    return total_dis / num_of_readings


def move_chassi(x, y, z, xy_speed, rot_speed):
    ep_chassis.move(x, y, z, xy_speed, rot_speed).wait_for_completed()


average_dis(1)


