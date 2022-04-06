import PySimpleGUI as sg

from main import*

"""
Basic GUI for Robomaster 
"""


def run_gui():
    sg.theme('Dark')
    # sg.set_options(element_padding=(3, 2))

    row_1 = sg.Frame('Movement:',
                     [[sg.Text('X-Axis(m):', pad=((10, 3), 25)), sg.Input(size=(6, 1), default_text='.3', key='-X-', enable_events=True,
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
    chosen_freq = 1

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

    # for key, state in {'-Start-': False}.items():
    #     window[key].update(disabled=state)

    while True:
        event, values = window.read()
        print(event, values)
        if event == sg.WIN_CLOSED:
            break
        elif event == '-GO-':
            move_chassi(float(values['-X-']), float(values['-Y-']), float(values['-ROTATION_DEG-']), float(values['-XY_SPEED-']),
                        float(values['-ROTATION_SPEED-']))
        elif event == '-N_SCAN-':
            window['-DIST_ARR-'].update(value=str(get_nway_dis(values['N'])))
        elif event == '-SCAN-':
            window['-DIST-'].update(value=average_dis(1))
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


run_gui()
