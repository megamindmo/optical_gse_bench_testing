from zaber_motion import Units
from zaber_motion.binary import Connection, CommandCode
import math 
import time

#use ls /dev | grep -E 'ttyUSB|ttyACM' when device is connected to find
#which port. 
class ZaberMirror:
  def __init__(self, connect):
    self.connection = connect
    device_list = self.connection.detect_devices()
    print("Found {} devices".format(len(device_list)))
    self.elevation_device = device_list[0]
    self.horizontal_device = device_list[1]
    self.horizontal_device.move_absolute(0)
    self.elevation_device.move_absolute(0)
    self.elevation_device.generic_command(CommandCode.SET_TARGET_SPEED,1000)
    self.horizontal_device.generic_command(CommandCode.SET_TARGET_SPEED,1000) 
    return
  
  def zero(self):
    print('zero')
    self.diag_move_absolute(0,0)
  
  def home(self):
    self.elevation_device.home()
    self.horizontal_device.home()
  
  def calibrate(self):
    """Calibrates the camera on start"""
    self.home()
    self.zero()

  def start(self):
    self.calibrate()
  
  def convert_microstep_to_angle(self,p_microsteps):
    """This converts absolute steps into angle. The formula is specified in the spec sheet of the device.
    :param p_microsteps: absolute steps
    :type :p_microsteps: int, there is a max step of 62000
    TODO double check the max step 
    :return: angular_mrad
    :rtype: float, micro radians"""
    #Tan(dTheta/1000) = 0.09921875*(P/L)
    L = 66660
    angular_mrad = 1000*math.atan(0.09921875 * (p_microsteps/L))
    return angular_mrad

  def diag_move_absolute(self,pos1,pos2,timeout=100):
    """This produces a diagonal movement to absolute position set by the user.
    
    :param dev1: Motor 
    :type dev1: Device
    
    :param dev2: Motor
    :type dev2: Device
    
    :param pos1: Position of dev1 Device
    :type pos1: int, maximum of 62000
    
    :param pos2: Position of dev2 Device
    :type pos2: int, maximum of 62000
    
    :param timeout: this sets the timeout for the device. If it takes longer than the set time out to reach the absolute position and error will be thrown. 
    :type timeout: int, seconds

    :return: None
    :rtype: None
    """
    self.horizontal_device.generic_command_no_response(CommandCode.MOVE_ABSOLUTE,pos1)
    self.elevation_device.generic_command(CommandCode.MOVE_ABSOLUTE,pos2,timeout)
    return None
  
  def display_position(self, ):
    """This prints into the command line the position of devices
    
    :param dev1: Motor 
    :type dev1: Device
    :param dev2: Motor
    :type dev2: Device
    :return: A tuple of dev1 and dev2 position
    :rtype: tuple
    """
    
    print(self.horizontal_device.get_position(),self.elevation_device.get_position())
    return self.horizontal_device.get_position(),self.elevation_device.get_position()
  
  def cross_move(self,bound=10000):
    """cross move function allows us to make X movements with the laser. 
    :param: dev1: This would be a motor device
    :type dev1: Device
    :param: dev2: This would be another motor device
    :type dev2: Device

    :param bound: Describe the abosulte position bound, defaults to 1000
    :type bound: int 

    NOTE use the microstep to angle to convert the bound to angle.
    TODO: Check if 1 absolute = 1 Microstep some modules have 1 abosulte set to 60 microsteps.
    """
    self.horizontal_device.move_absolute(0)
    self.elevation_device.move_absolute(0)
    bounding_box = [
      (bound,bound),
      (-bound,-bound),
      (bound,-bound),
      (-bound,bound),
    ]
    for vertix in bounding_box:
      self.diag_move_absolute(vertix[0],vertix[1])
      time.sleep(0.2)
      self.display_position()
      self.diag_move_absolute(0,0)
      time.sleep(0.2)
      self.display_position()

  def connect_device(self,):
        
    with Connection.open_serial_port("/dev/ttyUSB0") as connection:
      """NOTE there is different spec for ASCII and Binary. We are using Binary"""
      device_list = connection.detect_devices()
      print("Found {} devices".format(len(device_list)))
      device_EL = device_list[0]
      device_HZ = device_list[1]
      #NOTE Uncomment this when doing a real run. It calibrates the mirror to home position so that absolute zero position is set correctly.  
      # device_EL.home()
      # device_HZ.home()
      device_EL.generic_command(CommandCode.SET_TARGET_SPEED,1000)
      device_HZ.generic_command(CommandCode.SET_TARGET_SPEED,1000)
      self.cross_move(device_HZ,device_EL,)
      
      # device_HZ.move_absolute(0)
      # device_EL.move_absolute(0)
      
      # device_HZ.generic_command_no_response(CommandCode.MOVE_ABSOLUTE,10000)
      # device_EL.generic_command_no_response(CommandCode.MOVE_ABSOLUTE,10000)
      #connection.generic_command(0, CommandCode.MOVE_TO_STORED_POSITION,10000,10)
      # device_EL.home()
      # device_EL.move_absolute(0)
      # device_HZ.home()
      # device_HZ.move_absolute(0)
      
      # connection.generic_command_with_units(1,CommandCode.SET_TARGET_SPEED,1000,10,)
      # connection.generic_command(1,CommandCode.HOME,0,10)
      # connection.generic_command(1,CommandCode.MOVE_ABSOLUTE,0,10)


      # device_EL = device_list[0]
      # device_HZ = device_list[1]
      # print(device_HZ.move_velocity(5),device_EL.move_velocity(5))
      # #lists all the functions we have with the device
      # # print(dir(device))
      # # #moves to absolute zero
      # # device.move_absolute(0)
      # device_EL.home()
      # device_HZ.home()
      # connection.
      
      # time.sleep(2)
      # device_EL.move_absolute(0)
      # device_HZ.move_absolute(0)
      # time.sleep(2)
      # print(device_HZ.get_position())
      # left_to_right(device_HZ)
      # # device_EL.move_relative(40000)
  def post_request_handler(self,data):
    if 'POS' in data:
      if type(data['POS']) is tuple:
        print("DATA BEING RECIEVD:",data['POS'])
        self.diag_move_absolute(data['POS'][0],data['POS'][1])
      else:
        match data['POS']:
          case 'Zero':
            print("entering the zero match")
            self.zero()
          case 'Home':
            self.home()
          case 'Cross Mode':
            self.cross_move() 
    
if __name__ == "__main__":
  zaber_port = "/dev/ttyUSB0"
  with Connection.open_serial_port(zaber_port) as connection:
    test_mirror = ZaberMirror(connection)
    test_mirror.zero()
    test_mirror.display_position()
    test_mirror.home()
    test_mirror.display_position()


