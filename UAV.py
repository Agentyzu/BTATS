# -*- coding: utf-8 -*-
"""
@Time ： 2023-09-29 21:20
@Auth ： Huailing Ma
@File ：UAV.py
@IDE ：PyCharm
@Motto：ABC(Always Be Coding)
"""

from ToolHelper import ToolHelper
from random import *
ToolHelper = ToolHelper(0, 0)

class UAV:
    """This class represents functions related to UAV, including utility computation and allocation

            Attributes:
                        idy         The selected UAV number
                        ability     The ability of UAVs
    """

    def __init__(self, idy, ability):
        self.idy = idy
        self.ability = ability

    # Stores UAV information
    def store(self):
        uav_arr = [self.idy, self.ability]
        return uav_arr


class UAVGroup:
    """This class represents functions related to UAV, including utility computation and allocation

            Attributes:
                        work_level         The selected UAV number
                        uav_array     The ability of UAVs
    """
    def __init__(self, work_level):
        self.work_level = work_level
        self.uav_array = []

    # Stores UAV groups information
    def uav_arr(self):
        uav_num = ToolHelper.task_num[self.work_level] * ToolHelper.multiple[self.work_level]
        for i in range(0, uav_num):
            ability = randint(ToolHelper.ability[self.work_level][0], ToolHelper.ability[self.work_level][1])
            uav = UAV(i, ability)
            self.uav_array.append(uav.store())
        return self.uav_array

    # Calculates the total abilities
    def sum_i(self):
        total = 0
        for i in range(len(self.uav_array)):
            total += self.uav_array[i][1]
        return total

