import math

from robomaster import robot
import PySimpleGUI as sg
import time
import os
import CGALPY_add_dlls

import simple_motion_planning

os.add_dll_directory("C:/Users/Alon/Documents/Robot/FDML-Build/src/libs/fdml/Release")
import fdmlpy
import importlib
import vbfdml_example

"""
Basic GUI for Robomaster 
"""

# sg.theme('Dark')
# todo:  distance from sensors 22.5cm, decrease 22.5/2 from distance[0] and increase from distance[1]
# sg.set_options(element_padding=(3, 2))


col = sg.Frame('Locate and Travel:',
                 [[sg.Text('Number of measurements:', pad=((20, 3), 30)),
                   sg.Input(size=(6, 1), default_text='4', key='-N-',
                            background_color='white',
                            text_color='black'),
                   sg.Button('Go', key='-loc_move-', size=(20, 3))
                   ],
                  [sg.Checkbox('Show location on map', default=False, key='show_location')]])

layout = [[col]]

window = sg.Window("Robo", layout,
                   default_element_size=(15, 15),
                   # text_justification='center',
                   auto_size_text=True,
                   auto_size_buttons=True,
                   element_justification='center',
                   finalize=True
                   )

"""
Robomaster 
"""

ep_robot = robot.Robot()

connected = ep_robot.initialize(conn_type="ap")

ep_chassis = ep_robot.chassis
ep_version = ep_robot.get_version()
print("Robot Version: {0}".format(ep_version))



class Robot_Params:

    def __init__(self, front_direction_dis_arr, back_direction_dis_arr, nway_dist_arr, n_way, cur_dist, cur_avg_dist):
        self.front_direction_dis_arr = front_direction_dis_arr
        self.back_direction_dis_arr = back_direction_dis_arr
        self.nway_dist_arr = nway_dist_arr
        self.n_way = n_way
        self.cur_dist = cur_dist
        self.cur_avg_dist = cur_avg_dist


    def measure_handler(self, dis_arr):
        if len(self.nway_dist_arr) == int(self.n_way):  # finished n-way measure
            print(f"{self.n_way}-way distance array: ", self.nway_dist_arr)
            return

        if len(self.front_direction_dis_arr) == 5:  # 5 samples average
            avg_front = sum(self.front_direction_dis_arr) / len(self.front_direction_dis_arr)
            avg_back = sum(self.back_direction_dis_arr) / len(self.back_direction_dis_arr)
            self.nway_dist_arr.append([avg_front, avg_back])
            print(f"{self.n_way}-way distance array: ", self.nway_dist_arr)
            self.front_direction_dis_arr = []
            self.back_direction_dis_arr = []
            move_chassi(0, 0, 183 / int(self.n_way), rot_speed=80)  # change +1 in relation to 6/
            return
        cur_dist = (dis_arr[0] + 80) / 1000  # front sensor 8cm from center
        self.front_direction_dis_arr.append(cur_dist)
        cur_back_dis = (dis_arr[1] + 125) / 1000  # back sensor 8cm from center
        self.back_direction_dis_arr.append(cur_back_dis)
        print("one_direction_dist_arr: ", self.front_direction_dis_arr)


def nway_measure_distance(n_scan):
    ep_robot.sensor.sub_distance(freq=5,
                                 callback=n_scan.measure_handler)
    time.sleep(2.5 * int(n_scan.n_way))  # sleep time is crucial
    ep_robot.sensor.unsub_distance()


def move_chassi(x, y, z, xy_speed=0.5, rot_speed=30.0):
    ep_chassis.move(x, y, z, xy_speed, rot_speed).wait_for_completed()


def listener():
    # for key, state in {'-Start-': False}.items():
    #     window[key].update(disabled=state)

    while True:
        event, values = window.read()
        print(event, values)
        if event == sg.WIN_CLOSED:
            break
        elif event == '-GO-':
            move_chassi(float(values['-X-']), float(values['-Y-']), float(values['-ROTATION_DEG-']),
                        float(values['-XY_SPEED-']),
                        float(values['-ROTATION_SPEED-']))
        elif event == '-loc_move-':
            n_scan = Robot_Params([], [], [], values['-N-']/2, 0, 0)
            nway_measure_distance(n_scan)
            print(f"finished n_scan")
            flat_dist_list = [round(dis, 2) for sublist in n_scan.nway_dist_arr for dis in sublist]
            window['-DIST_ARR-'].update(f'Output = {flat_dist_list}')
            print(flat_dist_list)
            preds = vbfdml_example.find_location(flat_dist_list, values['-show_location-'])
            for pred in preds:
                print(pred.x, pred.y, pred.theta)
            print("next phase")
            degrees_from_X_axis = math.degrees(pred.theta)
            ep_chassis.move(0, 0, 270-degrees_from_X_axis, 0, 30).wait_for_completed()
            location = preds[0]
            moves = simple_motion_planning.find_path(location.x, location.y)
            for move in moves:
                ep_chassis.move(move[0], move[1], 0, 0.7, 0).wait_for_completed()
            # party mode

    ep_robot.close()
    window.close()


listener()
