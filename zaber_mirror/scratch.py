
import math
def convert_microstep_to_angle(p_microsteps):
    """This converts absolute steps into angle. The formula is specified in the spec sheet of the device.
    :param p_microsteps: absolute steps
    :type :p_microsteps: int, there is a max step of 62000
    TODO double check the max step 
    :return: angular_mrad
    :rtype: float, milli radians"""
    #Tan(dTheta/1000) = 0.09921875*(P/L)
    L = 66660
    angular_mrad = 1000*math.atan(0.09921875 * (p_microsteps/L))
    math.degrees(angular_mrad)
    return angular_mrad
print(convert_microstep_to_angle(11727.0))