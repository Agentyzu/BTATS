# -*- coding: utf-8 -*-
"""
@Time ： 2023-09-29 21:20
@Auth ： Huailing Ma
@File ：ToolHelper.py
@IDE ：PyCharm
@Motto：ABC(Always Be Coding)
"""

from configparser import ConfigParser
from numpy import *
from random import *

class ToolHelper():
    'This class represents the useful tools used in the program'

    # This function configures initialization parameters
    def __init__(self, task_arr, total_ability):
        config = ConfigParser()
        config.read('config.ini')
        self.task_sNum = config.getint('Experiment1', 'task_sNum')
        self.UAV_sMultiple = config.getint('Experiment1', 'UAV_sMultiple')
        self.task_wNum = config.getint('Experiment1', 'task_wNum')
        self.c_iter = config.getint('Experiment1', 'c_iter')
        self.gp_iter = config.getint('Experiment1', 'gp_iter')
        self.UAV_wMultiple = config.getint('Experiment1', 'UAV_wMultiple')
        self.weak_ability_l = config.getint('Ability', 'weak_ability_l')
        self.weak_ability_h = config.getint('Ability', 'weak_ability_h')
        self.strong_ability_l = config.getint('Ability', 'strong_ability_l')
        self.strong_ability_h = config.getint('Ability', 'strong_ability_h')
        self.delta = config.getint('Config', 'delta')
        self.learn_rate = config.getfloat('Config', 'learn_rate')
        self.B_strong = config.getint('Config', 'B_strong')
        self.B_weak = config.getint('Config', 'B_weak')
        self.iter_avg = config.getint('Config', 'iter_avg')
        self.weak_NData_l = config.getint('Data_num', 'weak_NData_l')
        self.weak_NData_h = config.getint('Data_num', 'weak_NData_h')
        self.strong_NData_l = config.getint('Data_num', 'strong_NData_l')
        self.strong_NData_h = config.getint('Data_num', 'strong_NData_h')
        self.value_coefficient = config.getfloat('Data_num', 'value_coefficient')
        self.b_total = {'strong': [20, 25], 'weak': [15, 20]}
        self.task_num = {'strong': 4, 'weak': 3}
        self.multiple = {'strong': 2, 'weak': 1}
        self.data = {'strong': [15, 25], 'weak': [5, 15]}
        self.ability = {'strong': [10, 15], 'weak': [5, 10]}
        self.a = [10, 15]
        self.zeta = [0.3, 0.8]
        self.task_arr = task_arr
        self.total_ability = total_ability

    # The list of alpha
    def alpha_arr(self):
        alpha_arr = []
        for i in self.task_arr:
            alpha_arr.append(i[-1][1])
        return alpha_arr

    # The list of distribution for abilities
    def distribution_initial(self):
        dis_ini = []
        for i in self.task_arr:
            lam = i[-1][-2]
            mu = i[-1][-1]
            dis_ini.append([i[0], round(lam * self.total_ability), round(mu * self.total_ability)])
        return dis_ini

    # The list of lambda
    def lam_arr(self):
        return [i[-1][-2] for i in self.task_arr]

    # Random partition
    def random_partition(self, total_sum, n):
        # Generate n-1 random integers representing n-1 split points
        partitions = sorted(sample(range(1, total_sum), n - 1))
        parts = [partitions[0]] + [partitions[i] - partitions[i - 1] for i in range(1, n - 1)] + [
            total_sum - partitions[-1]]
        return parts

    # Calculate the variance
    def calculate_variance(self, ul_arr):
        n = len(ul_arr)
        mean = sum(ul_arr) / n
        variance = sum((x - mean) ** 2 for x in ul_arr) / (n - 1)
        return variance


