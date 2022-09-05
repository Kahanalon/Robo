import math
from robomaster import robot, led
import PySimpleGUI as sg
import time
import motion_planning
import find_location

"""
Basic GUI 
"""
sg.theme('Dark')
col = sg.Frame('Locate and Travel:',
               [[sg.Text('Number of measurements:', pad=((20, 3), 30)),
                 sg.Input(size=(6, 1), default_text='4', key='-N-',
                          background_color='white',
                          text_color='black'),
                 sg.Button('Go', key='-loc&move-', size=(20, 3))
                 ],
                [sg.Checkbox('Show location on map', default=False, key='show_location')]])

layout = [[col]]

window = sg.Window("Robo", layout,
                   default_element_size=(15, 15),
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


class EP_Robot:

    def __init__(self, front_direction_dis_arr, back_direction_dis_arr, nway_dist_arr, n_way):
        self.front_direction_dis_arr = front_direction_dis_arr
        self.back_direction_dis_arr = back_direction_dis_arr
        self.nway_dist_arr = nway_dist_arr
        self.n_way = n_way

    def measure_handler(self, dis_arr):
        if len(self.nway_dist_arr) == int(self.n_way):  # finished n-way measure
            return

        if len(self.front_direction_dis_arr) == 5:  # 5 samples average
            avg_front = sum(self.front_direction_dis_arr) / len(self.front_direction_dis_arr)
            avg_back = sum(self.back_direction_dis_arr) / len(self.back_direction_dis_arr)
            self.nway_dist_arr.append([avg_front, avg_back])
            self.front_direction_dis_arr = []
            self.back_direction_dis_arr = []
            if len(self.nway_dist_arr) != int(self.n_way):
                move_chassi(0, 0, 183 / int(self.n_way),
                            rot_speed=80)  # 183 behaves better than 180 due to wheel friction
            return
        cur_dist = (dis_arr[0] + 80) / 1000  # front sensor 8cm from center
        self.front_direction_dis_arr.append(cur_dist)
        cur_back_dis = (dis_arr[1] + 125) / 1000  # back sensor 12.5cm from center
        self.back_direction_dis_arr.append(cur_back_dis)


def nway_measure_distance(n_scan):
    ep_robot.sensor.sub_distance(freq=5,
                                 callback=n_scan.measure_handler)
    time.sleep(2.5 * int(n_scan.n_way))  # sleep time is crucial due to sensor behaviour
    ep_robot.sensor.unsub_distance()


def move_chassi(x, y, z, xy_speed=0.5, rot_speed=30.0):
    ep_chassis.move(x, y, z, xy_speed, rot_speed).wait_for_completed()


def party():
    ep_robot.play_audio('song.wav')
    ep_led = ep_robot.led
    ep_chassis.move(0, 0, 770, 0, 60)
    for i in range(0, 23):
        ep_led.set_led(comp=led.COMP_ALL, r=250, g=25, b=25, effect=led.EFFECT_ON)
        time.sleep(.3)
        ep_led.set_led(comp=led.COMP_ALL, r=0, g=250, b=250, effect=led.EFFECT_ON)
        time.sleep(.3)


def listener():
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        elif event == '-loc&move-':
            n_scan = EP_Robot([], [], [], math.ceil(int(values['-N-']) / 2))
            nway_measure_distance(n_scan)
            flat_dist_list = [round(dis, 2) for sublist in n_scan.nway_dist_arr for dis in sublist]
            preds = find_location.find_location(flat_dist_list, values['show_location'])
            if len(preds) != 0:
                location = preds[0]
                theta = location.theta
                degrees_from_X_axis = math.degrees(theta)
                ep_chassis.move(0, 0, -degrees_from_X_axis, 0, 60).wait_for_completed()
                # ep_chassis.move(0.8 - location.y, 2.8 - location.x, 0, 0.7, 0).wait_for_completed()
                moves = motion_planning.find_path(location.x, location.y)
                print(f'moves relative to robot: {moves}')
                for move in moves:
                    ep_chassis.move(float(str(move[1])), float(str(move[0])), 0, 0.7, 0).wait_for_completed()
                # party()

    ep_robot.close()
    window.close()


listener()
