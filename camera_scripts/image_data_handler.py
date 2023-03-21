from camera_main.camera_capture import acquire_image
from analysis_scripts import center_of_beam
from PIL import Image
from datetime import date,datetime
import yaml

"""
The purpose of this script is to centralise the handling of image data and information. It will act as an
intermediary between the script operating the mvIMAPCT SDK and the data processing of other scripts. 
"""
data = []
with open('/home/mohamedm/Documents/Optical GSE/optical_gse_bench_testing/camera_scripts/parameters.yaml') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)

def get_image_from_camera():
    """This will get the raw image np array data."""
    return acquire_image()
     

def get_centroid(arr):
    """This will get the centroid of the array image."""
    return center_of_beam.main(arr)

def get_stats():
    """This will get all stats that the user has defined."""
    pass

def save_image(arr):
    """This will save the image into a local image folder."""
    img = array_to_image(arr)
    file_path = data['image_folder']+"/{}".format(date.today())
    img.save(file_path+"img_{}".format(datetime.now()))
    return  

def array_to_image(arr):
    return Image.fromarray(arr)

