import matplotlib.pyplot as plt
from camera_scripts import image_data_handler

def gui_post_camera(device,event_name,data):
    pass

def gui_zaber_post(device,event_name,data):
    "This should make post request to change the state of zaber"
    post_msg = {'POS':data}
    if not (data):
        post_msg = {'POS':event_name} 
    device.post_request_handler(post_msg)
    return 

def gui_get_camera_image_array():
    image_array = image_data_handler.acquire_image()
    return image_array

def gui_get_quad(device,event_name):
    pass
def gui_get_zaber(device,event_name):
    pass

#Helper Functions
def generate_fig(plot_var,x=0,y=0,):
    image = gui_get_camera_image_array()
    # print("IMAGE PROCESSED")
    # plt.figure(1)
    # fig = plt.gcf()
    # DPI = fig.get_dpi()
    # # ------------------------------- you have to play with this size to reduce the movement error when the mouse hovers over the figure, it's close to canvas size
    # fig.set_size_inches(404 * 2 / float(DPI), 404 / float(DPI))
    # # -------------------------------
    #plt.imshow(image,cmap='gray')
    plot_var.clf()
    #plot_var.cla()
    center = image_data_handler.get_centroid(image)
    
    plt.plot( 2592/2,1944/2, "og", markersize=10)
    print("IMAGE PROCESSED 1", center[0])
    #return fig

    return plot_var.imshow(image,cmap='gray'),center
def update_axis(f):
    image = gui_get_camera_image_array()
    f.set_data(image)
