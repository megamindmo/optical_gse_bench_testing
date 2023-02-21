import math
import yaml
from yaml.loader import SafeLoader
# centroid algorithm

def angle_perbutation(dx,dy,f):
    # Calculate angle of perbutation
    opp = math.sqrt((dx ** 2) + (dy ** 2))

    angle = math.atan(opp / f)
    # Convert to degrees and print result
    angle_degrees = math.degrees(angle)
    return angle_degrees

def pixel_displacement(x, y, x_center, y_center):
    #x_center and y_center represent the center pixel. x and y represent the centorid of beam.
    dx = abs(x-x_center)
    dy = abs(y-y_center)
    return dx,dy

def convert_pixel_to_distance(pixel_count, pixel_length):
    #converts a pixel count to distance
    return pixel_count*pixel_length

def main(x,y):
    with open('parameters.yaml') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    
    center_x = data['total_pix_width']/2
    center_y = data['total_pix_height']/2
    dx,dy = pixel_displacement(x,y,center_x,center_y)
    
    dx_meters = convert_pixel_to_distance(dx, data['pixel_length'])
    dy_meters = convert_pixel_to_distance(dy, data['pixel_length'])
    
    angle_perturb = angle_perbutation(dx_meters,dy_meters,data['focal_length'])
    
    return angle_perturb
    
if __name__ == "__main__":
    print(main(1287,972))
