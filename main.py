from robomaster import robot
import PySimpleGUI as sg
import time

"""
Basic GUI for Robomaster 
"""

sg.theme('Dark')

# sg.set_options(element_padding=(3, 2))

row_1 = sg.Frame('Movement:',
                 [[sg.Text('X-Axis(m):', pad=((10, 3), 25)),
                   sg.Input(size=(6, 1), default_text='.3', key='-X-',  # enable_events=True,
                            background_color='white', text_color='black'),
                   sg.Text('Y-Axis(m):', pad=((10, 3), 0)), sg.Input(size=(6, 1), default_text='.3', key='-Y-',
                                                                     background_color='white', text_color='black'),
                   sg.Text('Rotation(deg):', pad=((10, 3), 0)),
                   sg.Input(size=(6, 1), default_text='90', key='-ROTATION_DEG-',
                            background_color='white', text_color='black')]])

row_2 = sg.Frame('Speed:', [[sg.Text('XY-Speed(m/s) [0.5,2]:', pad=((10, 3), 20)),
                             sg.Input(size=(10, 1), default_text='1', key='-XY_SPEED-',
                                      background_color='white', text_color='black'),
                             sg.Text('Rotation(deg/sec) [10, 540]:', pad=((10, 3), 0)),
                             sg.Input(size=(10, 1), default_text='30', key='-ROTATION_SPEED-',
                                      background_color='white', text_color='black')]])

row_3 = sg.Frame('Sensor Freq(Hz):',
                 [[sg.Radio('1', 'Hz', default=True, key='-1hz-', size=(3, 1), enable_events=True),
                   sg.Radio('5', 'Hz', key='-5hz-', size=(3, 1), enable_events=True),
                   sg.Radio('10', 'Hz', key='-10hz-', size=(3, 1), enable_events=True),
                   sg.Radio('20', 'Hz', key='-20hz-', size=(3, 1), enable_events=True),
                   sg.Radio('50', 'Hz', key='-50hz-', size=(3, 1), enable_events=True),
                   sg.Text('Distance = ', key='-DIST-', size=(15, 1))]], )  # make in cm


row_4 = sg.Frame('', [[sg.Button('Go', key='-GO-', size=(10, 3)), sg.Button('Scan', key='-SCAN-', size=(10, 3))]],
                 border_width=0)

col_1 = sg.Frame('Manual Control:', [[row_1],
                                     [row_2],
                                     [row_3],
                                     [row_4]], element_justification='center')

col_2 = sg.Frame('Functions:',
                 [[sg.Text('n-way distance:', pad=((10, 3), 30)), sg.Input(size=(6, 1), default_text='4', key='-N-',
                                                                           background_color='white',
                                                                           text_color='black'),
                   sg.Button('Go', key='-N_SCAN-', size=(10, 3)),
                   sg.Text('Output = ', key='-DIST_ARR-', size=(15, 1))
                   ],
                  ])

layout = [[col_1],
          [col_2]]

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
chosen_freq = 1

class Robot_Params:

    def __init__(self, one_direction_dis_arr, nway_dist_arr, n_way, cur_dist, cur_avg_dist):
        self.one_direction_dis_arr = one_direction_dis_arr
        self.nway_dist_arr = nway_dist_arr
        self.n_way = n_way
        self.cur_dist = cur_dist
        self.cur_avg_dist = cur_avg_dist

    def measure_handler(self, dis_arr):
        if len(self.nway_dist_arr) == self.n_way:  # finished n-way measure
            print(f"{self.n_way}-way distance array: ", self.nway_dist_arr)
            return

        if len(self.one_direction_dis_arr) > 4:  # 5 samples average
            cur_avg_dist = sum(self.one_direction_dis_arr) / len(self.one_direction_dis_arr)
            print("cur_avg_dist is: ", cur_avg_dist)
            self.nway_dist_arr.append(cur_avg_dist)
            self.one_direction_dis_arr = []
            # move_chassi(0, 0, 90, rot_speed=100)
            return
        cur_dist = dis_arr[0]
        self.one_direction_dis_arr.append(cur_dist)
        print("one_direction_dist_arr: ", self.one_direction_dis_arr)


def nway_measure_distance(n_scan):
    ep_robot.sensor.sub_distance(freq=1,
                                 callback=n_scan.measure_handler)
    time.sleep(10)
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
        elif event == '-N_SCAN-':
            n_scan = Robot_Params([], [], values['-N-'], 0, 0)
            nway_measure_distance(n_scan)
            time.sleep(5)
            print(f"finished n_scan")
            values['-DIST_ARR-'] = f'Output = {n_scan.nway_dist_arr}'
            # try:
            #     params.nway_dist_arr.append(sum(params.one_direction_dis_arr) / len(params.one_direction_dis_arr))
            # except ZeroDivisionError as e:
            #     print("one_direction_dis_arr is empty. error: ", e)
            # print("nway: ", params.nway_dist_arr)
            # params.one_direction_dis_arr.clear()

            # window['-DIST_ARR-'].update(value=str(get_nway_dis(values['N'])))
        elif event == '-SCAN-':
            scan = Robot_Params([], [], 1, 0, 0)
            nway_measure_distance(scan)
            time.sleep(5)

            print(f"finished scan")

            # window['-DIST-'].update(value=cur_dist) check how to live update
        elif event == '-1hz-':
            chosen_freq = 1
        elif event == '-5hz-':
            chosen_freq = 5
        elif event == '-10hz-':
            chosen_freq = 10
        elif event == '-20hz-':
            chosen_freq = 20
        elif event == '-50hz-':
            chosen_freq = 50
        # elif event == ep_chassis.move(window['-X-'], window['-Y-'], window['-ROTATION_DEG-'], window['-XY_SPEED-'], window['-ROTATION_SPEED-']).wait_for_completed()'-Stop-' and recording:
        #     [window[key].update(disabled=value) for key, value in {
        #         '-Start-': False, '-Stop-': True, '-Reset-': False, '-Submit-': False}.items()]
        #     recording = False
        #     have_data = True
        # elif event == '-Reset-':
        #     [window[key].update(disabled=value) for key, value in {
        #         '-Start-': False, '-Stop-': True, '-Reset-': True, '-Submit-': True}.items()]
        #     recording = False
        #     have_data = False
        # elif event == '-Submit-' and have_data:
        #     [window[key].update(disabled=value) for key, value in {
        #         '-Start-': False, '-Stop-': True, '-Reset-': True, '-Submit-': False}.items()]
        #     recording = False

    window.close()


listener()
