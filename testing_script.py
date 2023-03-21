from quad_cell_scripts import quad_cell_handler
from zaber_mirror.mirror_controller import ZaberMirror
from zaber_motion.binary import Connection
import matplotlib.pyplot as plt
from data_scripts import quad_data as quad_handler
from testing_scripts.quad_cell_tests import movement_pattern
from influxdb_scripts import db
zaber_port = "/dev/ttyUSB3"

test_range = [(2800,0),(2800,-2000)]
angles = []
ch3 = []
ch4 = []
channel_map = {
    'ch1':0,
    'ch2':1,
    'ch3':2,
    'ch4':3,
}

def construct_data(lis,):
    samp = {'samp':
    {
        'ch1':lis[0],
        'ch2':lis[1],
        'ch3':lis[2],
        'ch4':lis[3],
    }}
    return samp 
        
def calibration_test(mirror):
    coord = movement_pattern.sample_rectangle(100)
    for i in range(len(coord)):
        mirror.post_request_handler({'POS':coord[i]})
        channels,std = quad_cell_handler.get_quad_cell_data()
        db.write_db(construct_data(channels))         


    pass

def plot_data(microstep_coordinates, mirror, channel1, channel2,angles):
    """
    :param channel1: represents the channel we want
    :type channel1: str, for example 'ch1'

    """
    channel1_data = []
    channel2_data = []
    # vector = (microstep_coordinates[1][0] - microstep_coordinates[0][0], microstep_coordinates[1][1] - microstep_coordinates[0][1])
    # vector_mag = (vector[0]**2 + vector[1]**2)**0.5
    # vector_norm = (vector[0]/vector_mag, vector[1]/vector_mag)
    # data_points = 10
    # step = vector_mag/data_points
    sampled_points = movement_pattern.sample_rectangle(1000)
    for i in range(data_points):
        # current_position_x = microstep_coordinates[0][0] + vector_norm*step*i
        # current_position_y = microstep_coordinates[0][1] + vector_norm*step*i
        # new_pos = (current_position_x,current_position_y)
        mirror.post_request_handler({'POS':new_pos})
        quad_data = quad_cell_handler.get_quad_cell_data()
        channel1_data += quad_data[channel_map[channel1]]
        channel2_data += quad_data[channel_map[channel2]]
        plt.scatter(i,channel1[-1],color = 'hotpink')
        plt.scatter(i, channel2[-1],color = '#88c999')
        plt.pause(0.05)
    quad_handler.write_file_dump(channel1_data, channel2_data,[0 for i in range(len(channel1_data))],[0 for i in range(len(channel1_data))])
    plt.show()

if __name__ == "__main__":
    with Connection.open_serial_port(zaber_port) as connection:
        fsm_device = ZaberMirror(connection)
        plot_data(test_range,fsm_device,'ch3','ch4',angles)
    pass

    
    
    