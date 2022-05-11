
import time
import PySimpleGUI as sg
import random


# ---------------- Settings for UI ------------

sg.theme('LightBrown13')   # Add a touch of color
font = ('Arial', 14)


#-------------------------- Main Function ---------------------
# Create the Window
def create_window(world):

 # now we start the main window

    if world['power state']:
        world['main state'] = 'sleep'

        status = 'Status: ' + 'sleep'

        layout0 = [ [sg.Image('UI/logo.png')], 
         [ sg.Text(status, key='status')  ], 
         [sg.Button('Wake Up' ,size=(10,1), pad=8)], 
         [sg.Button('Sleep',size=(10,1), pad=8 )],
         [sg.Button('Sex',size=(10,1), pad=8 )], 
         [sg.Button('Exit',size=(10,1), pad=8 )]]

        window = sg.Window("Hello World", layout0, element_justification='c', font=font) 

        while True:
            event, values = window.read(timeout=300)
            status = 'Status: ' + world['main state']
            window['status'].update(status)


            if event == sg.WIN_CLOSED or event == 'Exit': # if user closes window or clicks cancel
                world['power state'] = 0
                world['main state'] = 'shutdown'
                break

            if event == 'Wake Up':
                world['main state'] = 'awake'
                world['head motion'] = 'search'

            if event == 'Sleep':
                world['main state'] = 'sleep'

            if event == 'Sex':
                world['main state'] = 'sex'


#------------------ Smaller functions ------------------------

