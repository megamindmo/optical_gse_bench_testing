from quad_cell_scripts import quad_cell_handler
from zaber_mirror.mirror_controller import ZaberMirror
from zaber_motion.binary import Connection
import matplotlib.pyplot as plt
from data_scripts import quad_data as quad_handler
from testing_scripts.quad_cell_tests import movement_pattern
from influxdb_scripts import db
zaber_port = "/dev/ttyUSB3"
quad_cell_port = '/dev/ttyUSB0'
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

def construct_data(fields,field_vals,tags,tag_vals):
    samp = {'samp':{}}
    for i in range(len(fields)):
        samp['samp'][fields[i]] = field_vals[i]
    for j in range(len(tags)):
        samp['samp'][tags[j]] = tag_vals[j]

    return samp 

def db_test():
    fields =['a','b']
    field_vals = [5,10]
    tags = ['m','n']
    tag_vals = [1,0]
    point = db.write_db(construct_data(fields,field_vals,tags,tag_vals),
    fields=fields,
    tags=tags)

def calibration_test(mirror):
    coord = movement_pattern.sample_rectangle(100,x1=-1800,y1=-3500,x2=-1800,y2=1500)
    print("Number of points:",len(coord))
    db_list = []
    channel1_data = []
    channel2_data = []
    channel3_data = []
    channel4_data = []
    current_pos_x = []
    current_pos_y = [] 
    std_data = []
    for i in range(len(coord)):
        mirror.post_request_handler({'POS':(int(coord[i][0]),int(coord[i][1]))})
        print('CORD:',coord[i])
        channels,std = quad_cell_handler.get_quad_cell_data()
        print('quad:',channels," std:",std)
        # db.write_db(construct_data(channels))
        channel1_data.append(channels[0])
        channel2_data.append(channels[1])
        channel3_data.append(channels[2])
        channel4_data.append(channels[3])
        current_pos_x.append(int(coord[i][0]))
        current_pos_y.append(int(coord[i][1]))
        plt.scatter(i,channel1_data[-1],color = 'hotpink')
        plt.scatter(i, channel2_data[-1],color = '#88c999')
        plt.scatter(i, channel3_data[-1],color = 'blue')
        plt.scatter(i, channel4_data[-1],color = 'red')
        plt.pause(0.05)
        std_data.append(std)
    quad_handler.write_file_dump(current_pos_x,current_pos_y,channel1_data, channel2_data,channel3_data,channel4_data,std_data)         
    plt.show()

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
    for i in range(sampled_points):
        # current_position_x = microstep_coordinates[0][0] + vector_norm*step*i
        # current_position_y = microstep_coordinates[0][1] + vector_norm*step*i
        # new_pos = (current_position_x,current_position_y)
        mirror.post_request_handler({'POS':new_pos})
        print('position', new_pos)
        quad_data = quad_cell_handler.get_quad_cell_data()
        print('quadcell:',quad_data)
        channel1_data += quad_data[channel_map[channel1]]
        channel2_data += quad_data[channel_map[channel2]]
        plt.scatter(i,channel1[-1],color = 'hotpink')
        plt.scatter(i, channel2[-1],color = '#88c999')
        plt.pause(0.05)
    quad_handler.write_file_dump(channel1_data, channel2_data,[0 for i in range(len(channel1_data))],[0 for i in range(len(channel1_data))])
    plt.show()

if __name__ == "__main__":
    # db_test()
     with Connection.open_serial_port(zaber_port) as connection:
         fsm_device = ZaberMirror(connection)
         calibration_test(fsm_device)
    # pass

    
    
    