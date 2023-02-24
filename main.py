from zaber_mirror.mirror_example import ZaberMirror
from gui import ExperimentDisplay
from zaber_motion.binary import Connection

camera_device = 0 
quad_cell = 0
zaber_port = "/dev/ttyUSB0"
with Connection.open_serial_port(zaber_port) as connection:
    fsm_device = ZaberMirror(connection)
    user_interface_control = ExperimentDisplay(fsm_device,camera_device,quad_cell)
    while True:
        user_interface_control.launch()

