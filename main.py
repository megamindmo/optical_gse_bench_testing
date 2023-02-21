from zaber_mirror.mirror_example import ZaberMirror
from gui import ExperimentDisplay

fsm_device = ZaberMirror()
camera_device = 0 
quad_cell = 0
user_interface_control = ExperimentDisplay(fsm_device,camera_device,quad_cell)

while True:
    user_interface_control.launch()

