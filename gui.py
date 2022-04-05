import PySimpleGUI as sg
# from main import ep_chassis

"""
Demonstrates using a "tight" layout with a Dark theme.
Shows how button states can be controlled by a user application.  The program manages the disabled/enabled
states for buttons and changes the text color to show greyed-out (disabled) buttons
"""

sg.theme('Dark')
sg.set_options(element_padding=(3, 2))

layout = [[
    [[sg.Text('X-Axis:', pad=((0, 0), 0)), sg.Input(size=(10, 1), default_text='1', key='-X-',
                                                    background_color='white', text_color='black')],
     [sg.Text('Y-Axis:', pad=((0, 0), 0)), sg.Input(size=(10, 1), default_text='1', key='-Y-',
                                                    background_color='white', text_color='black')],
     [sg.Text('Rotation(deg):', pad=((0, 0), 0)), sg.Input(size=(10, 1), default_text='90', key='-ROTATION_DEG-', # enable_events
                                                           background_color='white', text_color='black')]],
    [sg.Text('XY-Speed(m/s) [0.5,2]:', pad=((0, 0), 0)), sg.Input(size=(10, 1), default_text='1', key='-XY_SPEED-',
                                                          background_color='white', text_color='black')],
    [sg.Text('Rotation-Speed(deg/sec) [10, 540]:', pad=((0, 0), 0)), sg.Input(size=(10, 1), default_text='30', key='-ROTATION_SPEED-',
                                                                    background_color='white', text_color='black')],
    [[sg.Frame('Sensor Freq(Hz):', [[sg.Radio('1', 'radio1', default=True, key='-1hz-', size=(3, 1)),
                                     sg.Radio('5', 'radio1', key='-5hz-', size=(3, 1)),
                                     sg.Radio('10', 'radio1', key='-10hz-', size=(3, 1)),
                                     sg.Radio('20', 'radio1', key='-20hz-', size=(3, 1)),
                                     sg.Radio('50', 'radio1', key='-50hz-', size=(3, 1))]], )]],
    [[sg.Button('Clear', key='-CLEAR-')], [sg.Button('Default')], [sg.Button('Go', key='-GO-')]]

]]

window = sg.Window("Robo", layout,
                   # default_element_size=(5, 5),
                   # text_justification='center',
                   auto_size_text=True,
                   auto_size_buttons=True,
                   # default_button_element_size=(12, 12),
                   # finalize=True
                   )

# for key, state in {'-Start-': False}.items():
#     window[key].update(disabled=state)

recording = have_data = False
while True:
    event, values = window.read()
    print(event, values)
    if event == sg.WIN_CLOSED:
        break
    # if event == '-GO-':
        # for key, state in {'-X-': 0, '-Y-': 0}.items():
        #     window[key] = state
        # recording = True
        # ep_chassis.move(window['-X-'], window['-Y-'], window['-ROTATION_DEG-'], window['-XY_SPEED-'], window['-ROTATION_SPEED-']).wait_for_completed()
    elif event == '-Stop-' and recording:
        [window[key].update(disabled=value) for key, value in {
            '-Start-': False, '-Stop-': True, '-Reset-': False, '-Submit-': False}.items()]
        recording = False
        have_data = True
    elif event == '-Reset-':
        [window[key].update(disabled=value) for key, value in {
            '-Start-': False, '-Stop-': True, '-Reset-': True, '-Submit-': True}.items()]
        recording = False
        have_data = False
    elif event == '-Submit-' and have_data:
        [window[key].update(disabled=value) for key, value in {
            '-Start-': False, '-Stop-': True, '-Reset-': True, '-Submit-': False}.items()]
        recording = False

window.close()
