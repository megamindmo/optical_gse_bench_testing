from PIL import Image
import numpy as np
import yaml
from yaml.loader import SafeLoader
import matplotlib.pyplot as plt


def calculate_center_of_mass(im_pixel_array,):
    x_val_row = np.arange(0,len(im_pixel_array[0]))
    x_val_row = x_val_row[np.newaxis, :]

    y_val_col = np.arange(0,len(im_pixel_array))
    y_val_col = y_val_col[:, np.newaxis]


    y_tot = np.multiply(im_pixel_array,y_val_col)
    x_tot = np.multiply(im_pixel_array,x_val_row)

    y_center =  np.sum(y_tot)/np.sum(im_pixel_array)
    x_center =  np.sum(x_tot)/np.sum(im_pixel_array)
    return x_center, y_center

def layer_show(image,x,y):
    plt.imshow(image,cmap='gray')
    plt.plot(x, y, "og", markersize=10)
    plt.show()
def generate_fig(image,x,y):
    plt.figure(1)
    fig = plt.gcf()
    DPI = fig.get_dpi()
    # ------------------------------- you have to play with this size to reduce the movement error when the mouse hovers over the figure, it's close to canvas size
    fig.set_size_inches(404 * 2 / float(DPI), 404 / float(DPI))
    # -------------------------------
    plt.imshow(image,cmap='gray')
    plt.plot(x, y, "og", markersize=10)
    return fig

def main_gen():
    with open('/home/mohamedm/Documents/Optical GSE/optical_gse_bench_testing/camera_scripts/parameters.yaml') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    
    im = Image.open(data['image'])
    im_pixel_array = np.array(im)
    x,y = calculate_center_of_mass(im_pixel_array)
    print(x,y)
    #layer_show(im_pixel_array,x,y)
    return generate_fig(im_pixel_array,x,y)


if __name__=="__main__":
    main_gen()