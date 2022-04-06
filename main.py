from robomaster import robot
import PySimpleGUI as sg

from gui import*


ep_robot = robot.Robot()

connected = ep_robot.initialize(conn_type="ap")

ep_chassis = ep_robot.chassis
ep_version = ep_robot.get_version()
print("Robot Version: {0}".format(ep_version))


if connected:
    run_gui()
    quit = False
    while not quit:
        inp = input("type q to quit: ").strip()
        if inp == "q":
            quit = True
            ep_robot.close()

else:
    print("ERROR - failed to connect")


def get_nway_dis(n):
    dist_array = []
    for i in range(n):
        dist_array.append(average_dis(5))  # 5 distance samples
        ep_chassis.move(0, 0, 360 / n, xy_speed=1, z_speed=30).wait_for_completed()
    return dist_array


def average_dis(num_of_readings):
    total_dis = 0
    while num_of_readings > 0:
        # ep_robot.sensor.sub_distance(freq=1, callback=lambda x: print(x))
        cur_dis = ep_robot.sensor.sub_distance(freq=1, callback=lambda x: print(x))
        # ep_robot.unsub_distance( )
        total_dis += cur_dis
        num_of_readings -= 1
    return total_dis / num_of_readings


def move_chassi(x, y, z, xy_speed, rot_speed):
    ep_chassis.move(x, y, z, xy_speed, rot_speed).wait_for_completed()





