from discopygal.bindings import *
from discopygal.solvers import Scene, RobotDisc, ObstaclePolygon
from discopygal.solvers.rrt import dRRT, collision_detection

X = 0
Y = 0


def main(x, y):
    scene = Scene()
    robo = RobotDisc(
        radius=FT(0.4),
        start=Point_2(FT(x), FT(y)),
        end=Point_2(FT(2.8), FT(0.8)))
    scene.add_robot(robo)

    # Add obstacle in the middle
    middle_obstacle = ObstaclePolygon(
        poly=Polygon_2([
            Point_2(FT(0.98), FT(9.146)),
            Point_2(FT(0.98), FT(7.06)),
            Point_2(FT(1.61), FT(7.06)),
            Point_2(FT(1.61), FT(9.06))
        ])
    )
    scene.add_obstacle(middle_obstacle)

    # Also add bounding walls
    left_wall = ObstaclePolygon(
        poly=Polygon_2([
            Point_2(FT(0), FT(0)),
            Point_2(FT(0), FT(9.285)),
            Point_2(FT(-1), FT(-9.285)),
            Point_2(FT(-1), FT(0))
        ])
    )
    top_wall = ObstaclePolygon(
        poly=Polygon_2([
            Point_2(FT(0), FT(9.28)),
            Point_2(FT(3.9), FT(8.75)),
            Point_2(FT(3.9), FT(10)),
            Point_2(FT(0), FT(10))
        ])
    )
    right_wall = ObstaclePolygon(
        poly=Polygon_2([
            Point_2(FT(3.9), FT(8.75)),
            Point_2(FT(5.27), FT(-0.18)),
            Point_2(FT(6), FT(-0.18)),
            Point_2(FT(6), FT(8.75))
        ])
    )

    bottom_wall = ObstaclePolygon(
        poly=Polygon_2([
            Point_2(FT(5.27), FT(-0.18)),
            Point_2(FT(0), FT(0)),
            Point_2(FT(0), FT(-1)),
            Point_2(FT(5.27), FT(-1))
        ])
    )
    scene.add_obstacle(left_wall)
    scene.add_obstacle(right_wall)
    scene.add_obstacle(top_wall)
    scene.add_obstacle(bottom_wall)
    scene.add_obstacle(middle_obstacle)

    # Find paths for the robot
    solver = dRRT(num_landmarks=100, prm_num_landmarks=200, prm_k=15)
    solver.load_scene(scene)
    path_collection = solver.solve()  # Returns a PathCollection object
    result = []
    for i, (robot, path) in enumerate(path_collection.paths.items()):
        for point in path.points:
            result.append(point.location)
    print(result)

    collisions = collision_detection.ObjectCollisionDetection([left_wall, right_wall, top_wall, bottom_wall], robo)
    # i=0
    # while len(result) > 2:
    #     if (i<len(result)-2):
    #         if isPath(result[i],result[i+2]):
    #             result.remove(result[i+1])
    #         else:
    #             i+=1
    #         continue
    #     break

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
