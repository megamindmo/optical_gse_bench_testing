import PySimpleGUI as sg
import tkinter as tk
import time


class ExperimentDisplay:
    def __init__(self,zaber,camera,quadcell):
        
        self.zaber = zaber
        self.camera = camera
        self.quad_cell = quadcell
        
        self.left_column = [
            [sg.Image(filename='image1.png',key="-CAMERA-")], 
            [sg.Image(filename='image1.png',key="-QUADCELL-")]
            ]
        self.quad_data =[[1,2,3],[1,2]]
        self.right_column = [
            [sg.Text('Position 1'), sg.InputText(size=(25, 1), enable_events=True, key="-POS1-")],
            [sg.Text('Position 2'), sg.InputText(size=(25, 1), enable_events=True, key="-POS2-")],
            [sg.Button('Set Custom Position'), sg.Button('Cross Mode'), sg.Button('Home'), sg.Button('Zero')],
            [sg.Text('Status'),sg.Text('NONE', key='MOTORSTATUS' )],
            [sg.Text('Offset of Centroid on Camera dx,dy'),sg.Text('NONE', key='LASER_CENTROID' )],
            [sg.Text('Offset of Centroid on Quad dx,dy'),sg.Text('NONE', key='LASER_CENTROID' )],
            [sg.Text('QUAD-CELL READING'),],
            [
                sg.Listbox(

                    self.quad_data, enable_events=True, size=(40, 20), key="-QUADCELL LIST-"
                )
            ],
        ]
        self.layout = [
            [sg.Column(self.left_column),sg.VSeperator(), sg.Column(self.right_column)]
        ]
        self.window = sg.Window('My PyGui Application', self.layout)

        self.camera_state = []
        self.quad_cell_state = []
        self.zaber_state = []
    
    def event_handler(self, event):
        print("event handling")
        self.window['MOTORSTATUS'].update(event)
        print(self.window['-POS1-'])
        match event:
            case 'Set Custom Position':
                self.zaber_post(event,(self.window['-POS1-'].Get,self.window['-POS2-'].Get))
            case 'Cross Mode':
                self.zaber_post(event,[])
            case 'Home':
                self.zaber_post(event,[])
            case 'Zero':
                self.zaber_post(event,[])

    def camera_post(self,event_name,data):
        print(event_name)
        return {'POST':''}
    
    def zaber_post(self,event_name,data):
        print(event_name, data)
        "This should make post request to change the state of zaber"
        post_msg = {'POS':data}
        if not (data):
            post_msg = {'POS':event_name} 
        self.zaber.post_request_handler(post_msg)
        return 
    
    def camera_get(self):
        """This should get the camera image and centroid data to display."""
        image =0
        centroid=0
        return image, centroid
    
    def zaber_get(self):
        "This should get data of the position and angular position to display."
        position=0
        angular_data=0
        return position, angular_data
    
    def quad_cell_get(self):
        return 0
        
    def launch(self,):
        event, values = self.window.read()
        if event == sg.WIN_CLOSED:
            self.end()
        self.event_handler(event)
        self.camera_get()
        self.zaber_get()
        self.quad_cell_get()
    
    def end(self):
        self.window.close()

# experiment = ExperimentDisplay(0,0,0)
# experiment.main()