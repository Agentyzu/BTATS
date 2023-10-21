# -*- coding: utf-8 -*-
"""
@Time ： 2023-09-29 21:20
@Auth ： Huailing Ma
@File ：Coalition.py
@IDE ：PyCharm
@Motto：ABC(Always Be Coding)
"""
from math import *
from ToolHelper import ToolHelper
from random import *
from scipy.optimize import minimize
from Order import Order
ToolHelper = ToolHelper(0, 0)

class DistributionAbilities:
    """This class represents functions related to Assign isomorphic work capabilities, including utility computation and allocation

            Attributes:
                task_arr        The list of the UAV
                dis_ini         The list of the distribution for abilities
                total_ability   The total abilities of the UAVs
    """

    def __init__(self, task_arr, dis_ini, total_ability):
        self.task_arr = task_arr
        self.dis_ini = dis_ini
        self.total_ability = total_ability

    # Returns the homogeneous working capacity of the initialization allocation
    def dis_before(self):
        # Arrays store the homogeneous ability to work with random allocations
        dis_before = self.dis_ini.copy()
        cnt = [i[1] for i in dis_before]
        rest = self.total_ability - sum(cnt)
        while rest > 0:
            j = randint(0, len(dis_before) - 1)
            rest -= 1
            dis_before[j][1] += 1
        dis_before = [i[1] for i in dis_before]
        return dis_before

    # Initialize the allocation of UAVs
    def random_partition(self, lam_arr, uav_arr):
        uav_arr_copy = [i[1] for i in uav_arr].copy()

        result = []
        total_sum = sum(uav_arr_copy)

        for i in range(len(lam_arr)):
            if i == len(lam_arr) - 1:
                # The last array, directly using the remaining data
                result.append(uav_arr_copy)
                break

            # Calculates the minimum sum of this array
            min_sum = lam_arr[i]
            max_sum = total_sum - sum(lam_arr[:i]) - min_sum

            # Randomly select the elements in the array so that their sum is within the appropriate range
            selected_elements = []
            current_sum = 0

            while current_sum < min_sum:
                element = choice(uav_arr_copy)
                if current_sum + element <= max_sum:
                    selected_elements.append(element)
                    current_sum += element
                    uav_arr_copy.remove(element)
                else:
                    # If you can't meet the requirements, start over
                    selected_elements = []
                    current_sum = 0

            result.append(selected_elements)

        return result


class BandwidthAllocation:
    """This class represents functions related to Bandwidth resource allocation, including utility computation and allocation

                Attributes:
                    dis_before        The list of the distribution for abilities
                    alpha_arr         The list of the alpha
                    task_arr          The total abilities of the UAVs
                    a                 Parameters of Shannon's formula
                    b_total           Total bandwidth resources
                    zeta              Loss factor
    """

    def __init__(self, dis_before, alpha_arr, task_arr, total_ability, a, b_total, zeta):
        self.dis_before = dis_before
        self.alpha_arr = alpha_arr
        self.task_arr = task_arr
        self.total_ability = total_ability
        self.a = a
        self.b_total = b_total
        self.zeta = zeta

    # The objective function for optimization
    def objective(self, b_arr):
        sum = 0
        for i in range(len(self.task_arr)):
            data_num = self.task_arr[i][1]
            value = self.task_arr[i][2]
            if b_arr[i] <= 0 or self.dis_before[i] <= 0:
                continue
            x = 1 + self.a / b_arr[i]
            rate = b_arr[i] * log(x, 2)
            if rate == 0:
                continue
            a = value * (self.zeta * self.alpha_arr[i]) / (self.dis_before[i] / self.total_ability)
            cnt = a / rate
            sum += cnt
        return sum

    # Define inequality constraints
    def constraint_ineq(self, b_arr):
        return [b_arr[i] - 0.0 for i in range(len(b_arr))]

    # Define equation constraints
    def constraint_eq(self, b_arr):
        return sum([b_arr[i] for i in range(len(b_arr))]) - self.b_total

    # Optimize operations
    def result(self, b_arr):
        # A dictionary that defines inequality constraints
        con_ineq = {'type': 'ineq', 'fun': self.constraint_ineq}

        # A dictionary that defines equation constraints
        con_eq = {'type': 'eq', 'fun': self.constraint_eq}

        # Use the minimize function to perform hybrid constraint optimization
        result = minimize(self.objective, b_arr, constraints=[con_ineq, con_eq], method='SLSQP')
        return result.fun, result.x

class FormCoalition:
    """This class represents functions related to coalitions forming, including utility computation and allocation

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

    def __init__(self, dis, task_arr, l_idy, h_idy, total_ability, alpha_arr, b_arr, a, zeta, b_total):
        self.dis = dis
        self.task_arr = task_arr
        self.l_idy = l_idy
        self.h_idy = h_idy
        self.alpha_arr = alpha_arr
        self.b_arr = b_arr
        self.total_ability = total_ability
        self.a = a
        self.zeta = zeta
        self.b_total = b_total

    # Form coalitions
    def form_coalition(self):
        # dis_al is the initial value, and DIS is a value that is continuously assigned according to the order
        for i in range(ToolHelper.c_iter):
            # Randomly select a coalition
            idy1 = randint(0, len(self.task_arr) - 1)
            idy2 = idy1
            while self.dis[idy1] == 0:
                idy1 = randint(0, len(self.task_arr) - 1)
            while idy1 == idy2:
                idy2 = randint(0, len(self.task_arr) - 1)
            ballo = BandwidthAllocation(self.dis, self.alpha_arr, self.task_arr, self.total_ability, self.a, self.b_total, self.zeta)
            new_b_arr = ballo.result(self.b_arr)[1]
            cnt = self.dis.copy()
            cnt[idy1] -= 1
            cnt[idy2] += 1
            ballo = BandwidthAllocation(cnt, self.alpha_arr, self.task_arr, self.total_ability, self.a, self.b_total, self.zeta)
            new_b_arr_after = ballo.result(self.b_arr)[1]
            order = Order(idy1, idy2, self.a, self.zeta)
            self.dis, state = order.isomorphic_order(self.l_idy, self.h_idy, self.task_arr, self.total_ability, self.dis,
                                     self.alpha_arr, new_b_arr, new_b_arr_after)
            if i == (ToolHelper.c_iter - 1):
                if state == 1:
                    final_b_arr = new_b_arr_after
                else:
                    final_b_arr = new_b_arr
        return self.dis, final_b_arr

    # Form coalitions in a selfish order
    def form_coalition_selfish(self, result):
        for i in range(ToolHelper.c_iter):
            # Randomly pick two different alliances
            idy1 = randint(0, len(self.task_arr) - 1)
            idy2 = idy1
            while len(result[idy1]) == 0:
                idy1 = randint(0, len(self.task_arr) - 1)
            while idy1 == idy2:
                idy2 = randint(0, len(self.task_arr) - 1)
            dis_selfish = [sum(i) for i in result]
            b_re = BandwidthAllocation(dis_selfish, self.alpha_arr, self.task_arr, self.total_ability, self.a, self.b_total, self.zeta)
            new_b_arr = b_re.result(self.b_arr)[1]
            # Randomly select one UAV in the IDY coalition
            uav = choice(result[idy1])
            # IDY2 coalition
            result[idy1].remove(uav)
            result[idy2].append(uav)
            dis_selfish_after = [sum(i) for i in result]
            b_re = BandwidthAllocation(dis_selfish_after, self.alpha_arr, self.task_arr, self.total_ability, self.a, self.b_total, self.zeta)
            new_b_arr_after = b_re.result(self.b_arr)[1]
            result[idy2].remove(uav)
            result[idy1].append(uav)
            order = Order(idy1, idy2, self.a, self.zeta)
            self.result, state = order.selfish_order(self.l_idy, self.h_idy, self.task_arr, self.total_ability, result,
                                                  self.alpha_arr, new_b_arr, new_b_arr_after, uav)
            if i == (ToolHelper.c_iter - 1):
                if state == 1:
                    final_b_arr = new_b_arr_after
                else:
                    final_b_arr = new_b_arr
        return self.result, final_b_arr

    # Form coalitions in a pareto order
    def form_coalition_pareto(self, result):
        for i in range(ToolHelper.c_iter):
            # Randomly pick two different coalitions
            idy1 = randint(0, len(self.task_arr) - 1)
            idy2 = idy1
            while len(result[idy1]) == 0:
                idy1 = randint(0, len(self.task_arr) - 1)
            while idy1 == idy2:
                idy2 = randint(0, len(self.task_arr) - 1)
            dis_pareto = [sum(i) for i in result]
            b_re = BandwidthAllocation(dis_pareto, self.alpha_arr, self.task_arr, self.total_ability, self.a, self.b_total, self.zeta)
            new_b_arr = b_re.result(self.b_arr)[1]
            new_b_arr_copy = new_b_arr.copy()
            # Randomly select one UAV in the IDY coalition
            uav = choice(result[idy1])
            # IDY2 coalition
            result[idy1].remove(uav)
            result[idy2].append(uav)
            dis_pareto_after = [sum(i) for i in result]
            b_re = BandwidthAllocation(dis_pareto_after, self.alpha_arr, self.task_arr, self.total_ability, self.a, self.b_total,
                         self.zeta)
            new_b_arr_after = b_re.result(new_b_arr_copy)[1]
            result[idy2].remove(uav)
            result[idy1].append(uav)
            order = Order(idy1, idy2, self.a, self.zeta)
            self.result, state = order.pareto_order(self.l_idy, self.h_idy, self.task_arr, self.total_ability, result,
                                                  self.alpha_arr, new_b_arr, new_b_arr_after, uav)
            if i == (ToolHelper.c_iter - 1):
                if state == 1:
                    final_b_arr = new_b_arr_after
                else:
                    final_b_arr = new_b_arr
        return self.result, final_b_arr

    # Coalitions are formed without optimization
    def form_non_optimization(self):
        for i in range(ToolHelper.c_iter):
            # Randomly pick two different coalitions
            idy1 = randint(0, len(self.task_arr) - 1)
            idy2 = idy1
            while self.dis[idy1] == 0:
                idy1 = randint(0, len(self.task_arr) - 1)
            while idy1 == idy2:
                idy2 = randint(0, len(self.task_arr) - 1)
            order = Order(idy1, idy2, self.a, self.zeta)
            self.dis, state = order.isomorphic_order(self.l_idy, self.h_idy, self.task_arr, self.total_ability, self.dis,
                                     self.alpha_arr, self.b_arr, self.b_arr)
        return self.dis


