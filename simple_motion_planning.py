import json

from discopygal.bindings import *
from discopygal.solvers import PathPoint, Scene, RobotDisc, ObstaclePolygon
from discopygal.solvers.rrt import dRRT


X = 0
Y = 0


def main(x,y):
    scene = Scene()

    # Illustration of the scene: 
    # Two disc robots in a room, with an obstacle seperating them
    # The goal of the robots is to switch positions
    ###############################
    #                             #
    #                             #
    #                             #
    #      0      ###      0      #
    #     000     ###     000     #
    #      0      ###      0      #
    #                             #
    #                             #
    #                             #
    ###############################

    # Add disc robot on the left that wants to go to the right
    roboti = RobotDisc(
        radius=FT(0.5),
        start=Point_2(FT(x), FT(y)),
        end=Point_2(FT(3.0), FT(3.0)))
    scene.add_robot(roboti)


    # Add obstacle in the middle
    middle_obstacle = ObstaclePolygon(
        poly=Polygon_2([
            Point_2(FT(-1), FT(-1)),
            Point_2(FT(-1), FT(1)),
            Point_2(FT(1), FT(1)),
            Point_2(FT(1), FT(-1))
        ])
    )
    scene.add_obstacle(middle_obstacle)

    # Also add bounding walls
    left_wall = ObstaclePolygon(
        poly=Polygon_2([
            Point_2(FT(-7), FT(-4)),
            Point_2(FT(-7), FT(4)),
            Point_2(FT(-6), FT(4)),
            Point_2(FT(-6), FT(-4))
        ])
    )
    right_wall = ObstaclePolygon(
        poly=Polygon_2([
            Point_2(FT(6), FT(-4)),
            Point_2(FT(6), FT(4)),
            Point_2(FT(7), FT(4)),
            Point_2(FT(7), FT(-4))
        ])
    )
    top_wall = ObstaclePolygon(
        poly=Polygon_2([
            Point_2(FT(-6), FT(3.5)),
            Point_2(FT(-6), FT(4)),
            Point_2(FT(6), FT(4)),
            Point_2(FT(6), FT(3.5))
        ])
    )
    bottom_wall = ObstaclePolygon(
        poly=Polygon_2([
            Point_2(FT(-6), FT(-4)),
            Point_2(FT(-6), FT(-3.5)),
            Point_2(FT(6), FT(-3.5)),
            Point_2(FT(6), FT(-4))
        ])
    )
    scene.add_obstacle(left_wall)
    scene.add_obstacle(right_wall)
    scene.add_obstacle(top_wall)
    scene.add_obstacle(bottom_wall)

    # Export the scene to file
    # with open('examples/scenes/simple_motion_planning_scene.json', 'w') as fp:
    #     json.dump(scene.to_dict(), fp)

    # "Solve" the scene (find paths for the robots)
    solver = dRRT(num_landmarks=100, prm_num_landmarks=200, prm_k=15)
    solver.load_scene(scene)
    path_collection = solver.solve() # Returns a PathCollection object
    result = []
    for i, (robot, path) in enumerate(path_collection.paths.items()):
        for point in path.points:
            result.append(point.location)
    print(result)
    return result

def find_path(x,y):
    global  X, Y
    X = x
    Y = y
    path = main(X,Y)
    moves = []
    for i in range(len(path)-1):
        x_move = path[i+1][0] - path[i][0]
        y_move = path[i+1][1] - path[i][1]
        moves.append([x_move,y_move])
    print(moves)
    return moves

find_path(3,1.5)