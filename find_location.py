import math
import matplotlib.pyplot as plt
import vbfdml

N = 70  # grid resolution - more accurate, more time.
USE_GPU = True
NUM_MEASUREMENTS = 0
distance_measures = []
show_map = False


def run_vbfdml(poly, be, ms, n):
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


def main():
    poly = vbfdml.Polygon2D()
    poly.load_from_file('map.poly')

    be = vbfdml.BoxExtent3(
        6.1, 10.1, 2.1 * math.pi,  # extent
        2.5, 4, 0  # offset
    )

    ms = []
    for i in range(NUM_MEASUREMENTS):
        ms.append(vbfdml.Measurement(distance_measures[i], (
                2 * i * math.pi / NUM_MEASUREMENTS)))  # A single measurement the robot did. Angles are given in radians.

    preds = run_vbfdml(poly, be, ms, N)  # Get a list of predictions
    if show_map:
        # Visuallize polygons and predictions
        visualize_polygon(poly)
        for pred in preds:
            visualize_prediction(pred)
        plt.show()
    return preds


def find_location(measures, show_location):
    global distance_measures, NUM_MEASUREMENTS, show_map
    show_map = show_location

    NUM_MEASUREMENTS = len(measures)
    order = []
    for i in range(NUM_MEASUREMENTS):
        if i % 2 == 0:
            order.append(measures[i])
    for i in range(NUM_MEASUREMENTS):
        if i % 2 == 1:
            order.append(measures[i])
    distance_measures = order
    preds = main()
    return preds

