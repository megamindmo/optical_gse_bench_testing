"""The goal will be to generate the different coordinates to visit."""
import yaml
from yaml.loader import SafeLoader
import numpy as np
import matplotlib.pyplot as plt

with open('/home/star/optical_gse_quad_cell_alignment/runner/optical_gse_bench_testing/testing_scripts/quad_cell_tests/params.yaml') as f:
    data = yaml.load(f, Loader=SafeLoader)
    print(data)

def straight_line_points(start,end,points):
    """
    :param start: the start coordinate
    :type start: tuple

    :param points: number of points to generate in between
    :type points: int
    """
    assert (start[0]-end[0])%points==0
    assert (start[1]-end[0])%points==0
    return list(zip(np.linspace(start[0],end[0],points),np.linspace(start[1],end[1],points)))

#preferably move the params in yaml
def sample_rectangle(X,x1=int(data['bounding_box']['bottom_x']), y1=int(data['bounding_box']['bottom_y']), x2=int(data['bounding_box']['top_x']), y2=int(data['bounding_box']['top_y'])):
    """
    :param X: The number of samples of the space defined,
    :type X: int

    :param x,y: Bounding box 
    :type x,y:int
    """
    # Calculate the width and height of the rectangle/square
    width = abs(x2 - x1)
    height = abs(y2 - y1)

    if width*height ==0:
        return straight_line_points((x1,y1),(x2,y2),X)
    
    # Calculate the number of points per row and column
    points_per_row = int(np.sqrt(X) * (width / max(width, height)))
    points_per_col = int(np.sqrt(X) * (height / max(width, height)))
    print("Points per row:",points_per_row)
    print("Points per column:",points_per_col)
    dx = width / points_per_row
    dy = height / points_per_col
    sampled_points = []
    for row in range(points_per_row):
        for column in range(points_per_col):
            x = x1 + dx*(row+0.5)
            y = y1 + (column + 0.5) * dy
            sampled_points.append((x, y))
    print("Total number of sample points:",len(sampled_points))
    
    return sampled_points
if __name__=="__main__":
    # x,y = zip(*sample_rectangle(1000))
    # print(x[-1],y[-1])
     points = sample_rectangle(100,0,0,2800,-5000)
     print((len(points)))
     print(points[1][0])
    # plt.scatter(x,y,)  
    # plt.show()