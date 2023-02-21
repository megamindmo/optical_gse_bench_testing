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


def main():
    with open('parameters.yaml') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    
    im = Image.open(data['image'])
    im_pixel_array = np.array(im)
    x,y = calculate_center_of_mass(im_pixel_array)
    print(x,y)
    layer_show(im_pixel_array,x,y)
    return x,y


if __name__=="__main__":
    main()