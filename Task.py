# -*- coding: utf-8 -*-
"""
@Time ： 2023-09-28 21:20
@Auth ： Huailing Ma
@File ：Task.py
@IDE ：PyCharm
@Motto：ABC(Always Be Coding)
"""

from math import *
from random import *
from ToolHelper import ToolHelper
ToolHelper = ToolHelper(0, 0)

class Task:
    """This class represents functions related to initializing the task information, including utility computation and allocation

           Attributes:
                        idy         The number of the selected UAV
                        a           Parameters of Shannon's formula
                        zeta        Loss factor
                        data_num    The amount of data to calculate per task
                        value       The value of each task
    """

    def __init__(self, idy, data_num, value, a, zeta):
        self.idy = idy
        self.data_num = data_num
        self.value = value
        self.a = a
        self.zeta = zeta

    # calculate transmission rate,a here represents the S/N signal-to-noise ratio
    def cal_rate(self, b_arr):
        if b_arr[self.idy] <= 0:
            return 0
        x = 1 + self.a / b_arr[self.idy]
        rate = b_arr[self.idy] * log(x, 2)
        return rate

    # calculate alpha
    def cal_alpha(self, b_arr):
        rate = self.cal_rate(b_arr)
        # lower critical value
        alpha_l = 1 - (self.zeta * self.data_num) / (self.value * rate)
        # higher critical value
        alpha_h = 1
        alpha = uniform(alpha_l, alpha_h)
        return rate, alpha

    # calculate variants lambda and mu, 需要传一个total ability的参数，在order里面的sum_i函数
    def cal_lam_mu(self, b_arr, ability_total):
        tp = self.cal_alpha(b_arr)
        rate = tp[0]
        alpha = tp[1]
        cnt_lam = (self.zeta * alpha * self.data_num) / (rate * self.value * ability_total)
        cnt_mu = (self.zeta * (alpha-1) * self.data_num) / (rate * self.value * ability_total)
        lam = sqrt(cnt_lam)
        mu = 0.5 + sqrt(cnt_mu + 0.25)
        return rate, alpha, lam, mu

    # Stores the information of a single task and returns an array
    def store(self, b_arr, ability_total):
        task_arr = [self.idy, self.data_num, self.value, self.cal_lam_mu(b_arr, ability_total)]
        return task_arr

class TaskGroup:
    """This class represents functions related to Initializing the task group information, including utility computation and allocation

            Attributes:
                        work_level         The level of work for each task
                        a                  Parameters of Shannon's formula
                        zeta               Loss factor
                        ability_total      The total abilities of the UAVs
                        b_arr              The list of bandwidth allocation
    """

    def __init__(self, work_level, ability_total, b_arr, a, zeta):
        self.work_level = work_level
        self.ability_total = ability_total
        self.b_arr = b_arr
        self.a = a
        self.zeta = zeta

    # The list of task
    def task_arr(self):
        task_arr = []
        for i in range(0, ToolHelper.task_num[self.work_level]):
            data = randint(ToolHelper.data[self.work_level][0], ToolHelper.data[self.work_level][1])
            task = Task(i, data, data * ToolHelper.value_coefficient, self.a, self.zeta)
            task_arr.append(task.store(self.b_arr, self.ability_total))
        return task_arr
