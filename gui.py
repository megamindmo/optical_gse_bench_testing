import PySimpleGUI as sg
import tkinter as tk
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np
from camera_scripts.center_of_beam import main_gen

class Toolbar(NavigationToolbar2Tk):
    def __init__(self, *args, **kwargs):
        super(Toolbar, self).__init__(*args, **kwargs)


class ExperimentDisplay:
    def __init__(self,zaber,camera,quadcell):
        
        self.zaber = zaber
        self.camera = camera
        self.quad_cell = quadcell
        
        self.left_column = [
            [sg.B('Plot'), sg.B('Exit')],
            [sg.Canvas(key='fig_cv',
                       # it's important that you set this size
                       size=(400 * 2, 400)
                       )],
            [sg.Image(filename='image1.png',key="-CAMERA-")], 
            [sg.Image(filename='image1.png',key="-QUADCELL-")]
            ]
        self.quad_data =[[1,2,3],[1,2]]
        self.right_column = [
            [sg.Text('Position 1'), sg.InputText(size=(25, 1), enable_events=True, key="-POS1-")],
            [sg.Text('Position 2'), sg.InputText(size=(25, 1), enable_events=True, key="-POS2-")],
            [sg.Button('Set Custom Position'), sg.Button('Cross Mode'), sg.Button('Home'), sg.Button('Zero')],
            [sg.Canvas(key='controls_cv')],

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

    def draw_figure_w_toolbar(self,canvas, fig, canvas_toolbar):
        if canvas.children:
            for child in canvas.winfo_children():
                child.destroy()
        if canvas_toolbar.children:
            for child in canvas_toolbar.winfo_children():
                child.destroy()
        figure_canvas_agg = FigureCanvasTkAgg(fig, master=canvas)
        figure_canvas_agg.draw()
        toolbar = Toolbar(figure_canvas_agg, canvas_toolbar)
        toolbar.update()
        figure_canvas_agg.get_tk_widget().pack(side='right', fill='both', expand=1)

    def event_handler(self, event,values):
        print("event handling")
        self.window['MOTORSTATUS'].update(event)
        print()
        match event:
            case 'Set Custom Position':
                self.zaber_post(event,(int(values['-POS1-']),int(values['-POS2-'])))
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
    def draw(self):
        plt.figure(1)
        fig = plt.gcf()
        DPI = fig.get_dpi()
        # ------------------------------- you have to play with this size to reduce the movement error when the mouse hovers over the figure, it's close to canvas size
        fig.set_size_inches(404 * 2 / float(DPI), 404 / float(DPI))
        # -------------------------------
        x = np.linspace(0, 2 * np.pi)
        y = np.sin(x)
        plt.plot(x, y)
        plt.title('y=sin(x)')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.grid()
        return fig


        
    def launch(self,):
        event, values = self.window.read()
        if event == sg.WIN_CLOSED:
            self.end()
        elif event == 'Plot':
            self.draw_figure_w_toolbar(self.window['fig_cv'].TKCanvas, main_gen(), self.window['controls_cv'].TKCanvas)
        self.event_handler(event,values)
        self.camera_get()
        self.zaber_get()
        self.quad_cell_get()
    
    def end(self):
        self.window.close()

# experiment = ExperimentDisplay(0,0,0)
# experiment.main()