class Robot_Params:

    def __init__(self, one_direction_dis_arr, nway_dist_arr, n_way, cur_dist, cur_avg_dist):
        self.one_direction_dis_arr = one_direction_dis_arr
        self.nway_dist_arr = nway_dist_arr
        self.n_way = n_way
        self.cur_dist = cur_dist
        self.cur_avg_dist = cur_avg_dist

    def measure_handler(self, dis_arr):
        if len(self.nway_dist_arr) == self.n_way:  # finished n-way measure
            print(f"{self.n_way}-way distance array: ", self.nway_dist_arr)
            return

        if len(self.one_direction_dis_arr) > 4:  # 5 samples average
            cur_avg_dist = sum(self.one_direction_dis_arr) / len(self.one_direction_dis_arr)
            print("cur_avg_dist is: ", cur_avg_dist)
            self.nway_dist_arr.append(cur_avg_dist)
            self.one_direction_dis_arr = []
            # move_chassi(0, 0, 90, rot_speed=100)
            return
        cur_dist = dis_arr[0]
        self.one_direction_dis_arr.append(cur_dist)
        print("one_direction_dist_arr: ", self.one_direction_dis_arr)


params = Robot_Params([], [], 4, 0, 0)
for i in range(25):
    params.measure_handler([i, 0, 0, 0])
