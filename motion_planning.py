from discopygal.bindings import *
from discopygal.solvers import Scene, RobotDisc, ObstaclePolygon
from discopygal.solvers.rrt import dRRT, collision_detection
from CGALPY.Ker import Segment_2
from prm import PRM
import json
import sys

X = 0
Y = 0


def main(x, y):
    with open("scene.json", "r") as fp:
        d = json.load(fp)
        print(d)
        scene = Scene.from_dict(d)
    solver = PRM(num_landmarks=200, k=15)
    solver.load_scene(scene)
    path_collection = solver.solve()  # Returns a PathCollection object
    result = []
    for i, (robot, path) in enumerate(path_collection.paths.items()):
        for point in path.points:
            result.append(point.location)
    print(result)

    i = 0
    map_with_robot = collision_detection.ObjectCollisionDetection(scene.obstacles, scene.robots[0])
    while len(result) > 2:
        if i < len(result) - 2:
            point1 = CGALPY.Ker.Point_2(result[i])
            point2 = CGALPY.Ker.Point_2(result[i + 1])
            cur_edge = Segment_2(point1, point2)
            if map_with_robot.is_edge_valid(cur_edge):  # edge: class:`Ker.Segment_2`
                result.remove(result[i + 1])
            else:
                i += 1
            continue
        break

    print(result)

    return result


def find_path(x, y):
    global X, Y
    X = x
    Y = y
    path = main(X, Y)
    moves = []
    for i in range(len(path) - 1):
        x_move = path[i + 1][0] - path[i][0]
        y_move = path[i + 1][1] - path[i][1]
        moves.append([x_move, y_move])
    return moves


find_path(4, 3)
