from robomaster import robot

ep_robot = robot.Robot()
connected = ep_robot.initialize(conn_type="ap")

if connected:
    print("connected")
else:
    print("ERROR - failed to connect")

ep_chassis = ep_robot.chassis

def get_nway_dis(n):
    dist_array = []
    for i in range(n):
        dist_array.append(average_dis(5))
        ep_chassis.move(0, 0, 360/n, xy_speed=1, z_speed=30).wait_for_completed()
    return dist_array


def average_dis(num_of_readings):
    total_dis = 0
    while num_of_readings > 0 :
        # ep_robot.sensor.sub_distance(freq=1, callback=lambda x: print(x))
        cur_dis = ep_robot.sensor.sub_distance(freq=1, callback=lambda x: print(x))[0]
        #ep_robot.unsub_distance( )
        total_dis += cur_dis
        num_of_readings -= 1
    return total_dis/num_of_readings


print(get_nway_dis(4))

# ep_robot.close()
