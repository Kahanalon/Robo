import math
import matplotlib.pyplot as plt

import vbfdml

N = 70
USE_GPU = True
NUM_MEASUREMENTS = 3 # Set to 3 to see more predictions3

def run_vbfdml(poly, be, ms, n):
    # Single measurements
    vbs = []
    for m in ms:
        vbs.append(vbfdml.single_measurement(poly, m, be, n, USE_GPU))

    # Intersect all preimages
    isect = vbs[0]
    for vb in vbs[1:]:
        isect = vbfdml.do_intersect(isect, vb, n, False, USE_GPU)
    
    # Apply polygon filter and predict
    isect = vbfdml.polygon_filter(poly, be, isect)
    return vbfdml.predict(isect, be)

def visualize_polygon(poly: vbfdml.Polygon2D):
    """
    Add a polygon plot to a given matplotlib figure
    """
    X = []
    Y = []
    for v in poly.get_vertices():
        X.append(v.x)
        Y.append(v.y)
    X.append(X[0])
    Y.append(Y[0])

    plt.plot(X, Y)

def visualize_prediction(pred: vbfdml.Prediction, arrow_size=0.075):
    """
    Add prediction arrow to a given matplotlib figure
    """
    x = pred.x
    y = pred.y
    dx = arrow_size * math.cos(pred.theta)
    dy = arrow_size * math.sin(pred.theta)
    plt.arrow(x, y, dx, dy, head_width=arrow_size) 



if __name__ == "__main__":
    # Load the polygon of Room 446
    poly = vbfdml.Polygon2D()
    poly.load_from_file('resources/lab.poly')

    # Set the extent of the room (always the angle range > 2pi)
    be = vbfdml.BoxExtent3(
        7, 5, 2.1 * math.pi, # extent
        1.5, 0, 0 # offset
    )

    # Generate four measurements
    angles = [0.0, math.pi / 2, math.pi, 3 * math.pi / 2]
    ds = [1,1,1,3] # Measurements returned from the robot
    ms = []
    for i in range(NUM_MEASUREMENTS):
        ms.append(vbfdml.Measurement(ds[i], angles[i]))

    # Get a list of predictions
    preds = run_vbfdml(poly, be, ms, N)

    # Visuallize polygons and predictions
    visualize_polygon(poly)
    for pred in preds:
        visualize_prediction(pred)
    plt.show()   
