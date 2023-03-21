from zaber_motion import Units
from zaber_motion.binary import Connection, CommandCode
import math
import time
import datetime
import matplotlib.pyplot as plt
from zaber_mirror.mirror_controller import ZaberMirror
from quad_cell_handler import get_quad_cell_data


angles = []
ch3 = []
ch4 = []
channel_map = {
    'ch1':0,
    'ch2':1,
    'ch3':2,
    'ch4':3,
  }

def unit_vector_and_mag(coord1,coord2):
    vector = (coord2[0] - coord1[0], coord2[1] - coord1[1])
    vector_mag = (vector[0]**2 + vector[1]**2)**0.5
    vector_norm = (vector[0]/vector_mag, vector[1]/vector_mag)
    return vector_norm, vector_mag
def update_position(x,y,vector,step_size,step):
    return x+vector[0]*step*step_size, y+vector[1]*step*step_size


def plot_data(coordinates, mirror, channel1, channel2,angles,data_points=2):

    """
    :param channel1: represents the channel we want
    :type channel1: str, for example 'ch1'

    """
    channel1_data = []
    channel2_data = []
    start = [coordinates[0],coordinates[1]]
    mirror.diag_move_absolute(start[0][0],start[0][1])
    for j in range(len(coordinates)-1):
      microstep_coordinates = [coordinates[j],coordinates[j+1]]
      vector_norm,vector_mag = unit_vector_and_mag(microstep_coordinates[0], microstep_coordinates[1])
      step = math.ceil(vector_mag/data_points)
      for i in range(1,data_points):
        current_position_x, current_position_y = update_position(microstep_coordinates[0][0],microstep_coordinates[0][1],vector_norm,step,i)
        new_pos = (current_position_x,current_position_y)
        mirror.diag_move_absolute(int(new_pos[0]),int(new_pos[1]))
        mirror.display_position()
        quad_data = get_quad_cell_data()
        
        print("New:",(current_position_x,current_position_y))
        
        channel1_data += [quad_data[channel_map[channel1]]]
        channel2_data += [quad_data[channel_map[channel2]]]
        
        plt.pause(0.01)
        plt.scatter([i for i in range(len(channel1_data))],channel1_data,color = 'hotpink')
        plt.scatter([i for i in range(len(channel2_data))],channel2_data,color = '#88c999')
    plt.show()
    

    file = open('itemsMar9-1200pm '+channel1+" "+channel2+'.txt','w')
    for j in range(len(channel1_data)):
      file.write(str(channel1_data[j])+" "+str(channel2_data[j])+"\n")
    file.close()
    
def generate_zig_zag():
  test_range = []
  flip = 0
  new_row = []
  for j in range(1):
    new_row=[]
    for i in range(11):
      new_row.append((1000*(i-5),1000*(j-5)))
    if flip:
      new_row.reverse()
      flip=0
    else:
      flip = 1
    test_range+=new_row
  return test_range

# if __name__=="__main__":  
#   test_range = generate_zig_zag()
#   zaber_port = "/dev/ttyUSB3"
#   print("Hello")
#   with Connection.open_serial_port(zaber_port) as connection:
#     test_mirror = ZaberMirror(connection)
#     test_mirror.display_position()
#     test_mirror.home()
#     test_mirror.display_position()
#     test_mirror.zero()
#     plot_data(test_range,test_mirror,'ch4','ch3',[])

      