from zaber_mirror.mirror_controller import ZaberMirror
from gui_scripts.gui import ExperimentDisplay
from zaber_motion.binary import Connection
from quad_cell_scripts import quad_cell_handler
from camera_scripts import image_data_handler


camera_device = 0 
quad_cell = 0
zaber_port = "/dev/ttyUSB0"
quad_cell_port = 0

with Connection.open_serial_port(zaber_port) as connection:
    fsm_device = ZaberMirror(connection)
    user_interface_control = ExperimentDisplay(fsm_device,camera_device,quad_cell)
    while True:
        user_interface_control.launch()

# user_interface_control = ExperimentDisplay(0,0,0)
# while True:
#     user_interface_control.launch()
