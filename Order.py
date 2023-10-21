# -*- coding: utf-8 -*-
"""
@Time ： 2023-09-28 21:20
@Auth ： Huailing Ma
@File ：Order.py
@IDE ：PyCharm
@Motto：ABC(Always Be Coding)
"""

from Task import Task

class UtilityCoalition:
    """This class represents functions related to calculating the utility value of the consortium, including utility computation and allocation

                    Attributes:
                        dis              The list of the distribution for abilities
                        task_arr         The list of the tasks
                        l_idy            The list of the UAVs with less working capacity than alpha
                        h_idy            The list of the UAVs with more working capacity than alpha
                        alpha_arr        The list of alpha for tasks
                        b_arr            The list of bandwidth for tasks
                        total_ability    The sum of the UAV's working capacity
                        a                Parameters of Shannon's formula
                        b_total          Total bandwidth resources
                        zeta             Loss factor
            """

    def __init__(self, l_idy, h_idy, task_arr, total_ability, dis, alpha_arr, b_arr, a, zeta):
        self.l_idy = l_idy
        self.h_idy = h_idy
        self.task_arr = task_arr
        self.total_ability = total_ability
        self.dis = dis
        self.alpha_arr = alpha_arr
        self.b_arr = b_arr
        self.a = a
        self.zeta = zeta

    # Calculate the utility of a single consortium
    def utility_single(self, idy):
        data_num = self.task_arr[idy][1]
        value = self.task_arr[idy][2]
        task = Task(idy, data_num, value, self.a, self.zeta)
        rate = task.cal_rate(self.b_arr)
        if self.dis[idy] == 0 or rate == 0:
            return 0
        revene = value * self.dis[idy] / data_num
        if idy in self.l_idy:
            tm = value * (self.zeta * self.alpha_arr[idy] * self.total_ability) / (self.dis[idy] * rate)
        else:
            tm = (self.zeta * (self.alpha_arr[idy] - 1)) / ((self.dis[idy] / self.total_ability - 1) * rate)
        u_single = revene - tm
        return u_single

    # Calculate the total utility
    def utility_total(self):
        total = 0
        for i in range(len(self.task_arr)):
            total += self.utility_single(i)
        return total

    # Calculate heterogeneous consortium utility
    def utility_single_Ht(self, idy, result):
        if sum(result[idy]) == 0:
            return 0
        data_num = self.task_arr[idy][1]
        value = self.task_arr[idy][2]
        task = Task(idy, data_num, value, self.a, self.zeta)
        rate = task.cal_rate(self.b_arr)
        revene = value * sum(result[idy]) / data_num
        if rate == 0:
            return 0
        if idy in self.l_idy:
            tm = value * (self.zeta * self.alpha_arr[idy] * self.total_ability) / (sum(result[idy]) * rate)
        else:
            tm = (self.zeta * (self.alpha_arr[idy] - 1)) / ((sum(result[idy]) / self.total_ability - 1) * rate)
        u_single = revene - tm
        return u_single

class Order:
    """This class represents functions related to orders, including utility computation and allocation

            Attributes:
                        idy1         The number of the selected UAV
                        idy2         The number of the selected UAV
                        a            Parameters of Shannon's formula
                        zeta         Loss factor
    """

    def __init__(self, idy1, idy2, a, zeta):
        self.idy1 = idy1
        self.idy2 = idy2
        self.a = a
        self.zeta = zeta

    # Homomorphic order
    def isomorphic_order(self, l_idy, h_idy, task_arr, total_ability, dis, alpha_arr, b_arr, b_arr_after):
        u_single = UtilityCoalition(l_idy, h_idy, task_arr, total_ability, dis, alpha_arr, b_arr, self.a, self.zeta)
        u_single1 = u_single.utility_single(self.idy1)
        s1 = u_single1 / dis[self.idy1]
        dis[self.idy1] -= 1
        dis[self.idy2] += 1
        u_single = UtilityCoalition(l_idy, h_idy, task_arr, total_ability, dis, alpha_arr, b_arr_after, self.a,
                                    self.zeta)
        u_single11 = u_single.utility_single(self.idy1)
        if dis[self.idy1] == 0:
            s11 = 0
        else:
            s11 = u_single11 / dis[self.idy1]
        a = s1 + (s1 - s11) * dis[self.idy1]
        dis[self.idy1] += 1
        dis[self.idy2] -= 1
        dis[self.idy2] += 1
        dis[self.idy1] -= 1
        u_single = UtilityCoalition(l_idy, h_idy, task_arr, total_ability, dis, alpha_arr, b_arr_after, self.a,
                                    self.zeta)
        u_single2 = u_single.utility_single(self.idy2)
        s2 = u_single2 / dis[self.idy2]
        u_single = UtilityCoalition(l_idy, h_idy, task_arr, total_ability, dis, alpha_arr, b_arr, self.a, self.zeta)
        u_single22 = u_single.utility_single(self.idy2)
        s22 = u_single22 / dis[self.idy2]
        b = s2 + (s2 - s22) * dis[self.idy2]
        dis[self.idy2] -= 1
        dis[self.idy1] += 1
        if a < b:
            dis[self.idy1] -= 1
            dis[self.idy2] += 1
            state = 1
        else:
            state = 0
        return dis, state

    # Selfish order
    def selfish_order(self, l_idy, h_idy, task_arr, total_ability, result, alpha_arr, b_arr, new_b_arr_after, uav):
        u_single = UtilityCoalition(l_idy, h_idy, task_arr, total_ability, result, alpha_arr, b_arr, self.a, self.zeta)
        # idy1联盟
        u_single1 = u_single.utility_single_Ht(self.idy1, result)
        s1 = u_single1 / len(result[self.idy1])
        # idy2联盟
        result[self.idy2].append(uav)
        result[self.idy1].remove(uav)
        u_single = UtilityCoalition(l_idy, h_idy, task_arr, total_ability, result, alpha_arr, new_b_arr_after, self.a, self.zeta)
        u_single2 = u_single.utility_single_Ht(self.idy2, result)
        s2 = u_single2 / len(result[self.idy2])
        result[self.idy1].append(uav)
        result[self.idy2].remove(uav)
        if s1 < s2:
            result[self.idy1].remove(uav)
            result[self.idy2].append(uav)
            state = 1
        else:
            state = 0
        return result, state

    # Pareto order
    def pareto_order(self, l_idy, h_idy, task_arr, total_ability, result, alpha_arr, b_arr, new_b_arr_after, uav):
        u_single = UtilityCoalition(l_idy, h_idy, task_arr, total_ability, result, alpha_arr, b_arr, self.a, self.zeta)
        # idy1联盟
        u_single1 = u_single.utility_single_Ht(self.idy1, result)
        s1 = u_single1 / len(result[self.idy1])
        u_single2_else = u_single.utility_single_Ht(self.idy2, result)
        if len(result[self.idy2]) != 0:
            s2_else = u_single2_else / len(result[self.idy2])
        else:
            s2_else = 0
        result[self.idy2].append(uav)
        result[self.idy1].remove(uav)
        u_single = UtilityCoalition(l_idy, h_idy, task_arr, total_ability, result, alpha_arr, new_b_arr_after, self.a, self.zeta)
        u_single2 = u_single.utility_single_Ht(self.idy2, result)
        s2 = u_single2 / len(result[self.idy2])
        u_single1_else = u_single.utility_single_Ht(self.idy1, result)
        if len(result[self.idy1]) != 0:
            s1_else = u_single1_else / len(result[self.idy1])
        else:
            s1_else = 0
        result[self.idy1].append(uav)
        result[self.idy2].remove(uav)
        if s1 * len(result[self.idy1]) + s2_else * len(result[self.idy2]) < s2 * (
                len(result[self.idy2]) + 1) + s1_else * (len(result[self.idy1]) - 1):
            result[self.idy1].remove(uav)
            result[self.idy2].append(uav)
            state = 1
        else:
            state = 0
        return result, state

