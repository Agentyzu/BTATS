# -*- coding: utf-8 -*-
"""
@Time ： 2023-09-29 21:20
@Auth ： Huailing Ma
@File ：Transfer.py
@IDE ：PyCharm
@Motto：ABC(Always Be Coding)
"""

class Transfer:
    """This class represents functions related to data transfer, including utility computation and allocation

               Attributes:
                            v_arr          The list of value
                            data_total     The total data of tasks
                            cur_dis_arr    The list of the current distribution
                            total_ability  The total abilities
        """

    def __init__(self, v_arr, data_total, cur_dis_arr, total_ability):
        self.v_arr = v_arr
        self.data_total = data_total
        self.cur_dis_arr = cur_dis_arr
        self.total_ability = total_ability

    # data transfer
    def data_tf(self):
        data_after = []
        total_arr = [self.v_arr[i] * self.cur_dis_arr[i] for i in range(len(self.v_arr))]
        total = sum(total_arr)
        for i in range(len(self.v_arr)):
            d_after = self.data_total * self.v_arr[i] * self.cur_dis_arr[i] / total
            data_after.append(d_after)
        return data_after


