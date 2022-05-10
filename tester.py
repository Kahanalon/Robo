# one_direction_dis_arr = []
# nway_dist_arr = []
# n = 4
# cur_dist = 0
# cur_avg_dist = 0

class Robot_Params:

    def __init__(self, one_direction_dis_arr, nway_dist_arr, n_way, cur_dist, cur_avg_dist):
        self.one_direction_dis_arr = one_direction_dis_arr
        self.nway_dist_arr = nway_dist_arr
        self.n_way = n_way
        self.cur_dist = cur_dist
        self.cur_avg_dist = cur_avg_dist


params = Robot_Params([], [], 4, 0, 0)


def measure_handler(dis_arr):
    # global one_direction_dis_arr
    # global nway_dist_arr
    # global cur_dist
    # global cur_avg_dist
    if len(params.nway_dist_arr) == params.n_way:  # finished n-way measure
        print(f"{params.n_way}-way distance array: ", params.nway_dist_arr)
        return

    if len(params.one_direction_dis_arr) > 4:  # 5 samples average
        cur_avg_dist = sum(params.one_direction_dis_arr) / len(params.one_direction_dis_arr)
        print("cur_avg_dist is: ", cur_avg_dist)
        params.nway_dist_arr.append(cur_avg_dist)
        params.one_direction_dis_arr = []
        # move_chassi(0, 0, 90, rot_speed=100)
        return
    cur_dist = dis_arr[0]
    params.one_direction_dis_arr.append(cur_dist)
    print("one_direction_dist_arr: ", params.one_direction_dis_arr)


for i in range(25):
    measure_handler([i, 0, 0, 0])
