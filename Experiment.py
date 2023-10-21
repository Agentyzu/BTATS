# -*- coding: utf-8 -*-
"""
@Time ： 2023-09-29 21:20
@Auth ： Huailing Ma
@File ：Experiment.py
@IDE ：PyCharm
@Motto：ABC(Always Be Coding)
"""

from UAV import UAVGroup
from Task import TaskGroup
from random import *
from Coalition import DistributionAbilities
from Coalition import FormCoalition
from Order import UtilityCoalition
from Coalition import BandwidthAllocation

# experiment 1
def experiment1_FADR():
    # for work_level in ['strong', 'weak']:
    for work_level in ['weak']:
        # The four algorithms arr_single store m arrays, each of which stores the utility value of each task
        arr_single1 = []
        arr_single2 = []
        arr_single3 = []
        arr_single4 = []
        from ToolHelper import ToolHelper
        ToolHelper = ToolHelper(0, 0)
        for m in range(ToolHelper.iter_avg):
            a = randint(ToolHelper.a[0], ToolHelper.a[1])
            b_total = randint(ToolHelper.b_total[work_level][0], ToolHelper.b_total[work_level][1])
            zeta = 0.4
            uav_array = UAVGroup(work_level)
            uav_arr = uav_array.uav_arr()
            total_ability = uav_array.sum_i()
            b_arr = ToolHelper.random_partition(b_total, ToolHelper.task_num[work_level])
            task_array = TaskGroup(work_level, total_ability, b_arr, a, zeta)
            task_arr = task_array.task_arr()
            from ToolHelper import ToolHelper
            ToolHelper = ToolHelper(task_arr, total_ability)
            dis_ini = ToolHelper.distribution_initial()
            alpha_arr = ToolHelper.alpha_arr()
            dis_be = DistributionAbilities(task_arr, dis_ini, total_ability)
            dis_before = dis_be.dis_before()
            lam_arr = ToolHelper.lam_arr()
            ballo = BandwidthAllocation(dis_before, alpha_arr, task_arr, total_ability, a, b_total, zeta)
            print('第几轮', m)
            for i in range(4):
                b_arr_copy = b_arr.copy()
                if i == 0:
                    new_b_arr = ballo.result(b_arr_copy)[1]
                    l_idy = [i for i in range(len(task_arr))]
                    h_idy = []
                    form = FormCoalition(dis_before, task_arr, l_idy, h_idy, total_ability, alpha_arr, new_b_arr, a,
                                         zeta, b_total)
                    # An array of allocations for homogeneous working capacity
                    dis, final_b_arr = form.form_coalition()
                    print('dis', dis)
                    # Find the subset and difference, the selected subset is subset, the difference between the subset and the target value is diff
                    from Iconversion import HeterogeneousTrans
                    h_trans = HeterogeneousTrans()
                    diff_arr = []
                    len_subset_arr = []
                    for p in range(len(dis)):
                        if p == 0:
                            nums = [j[1] for j in uav_arr]
                        subset, diff, nums = h_trans.find_subset(nums, dis[p])
                        len_subset_arr.append(len(subset))
                        diff_arr.append(diff)
                    from Transfer import Transfer

                    v_arr = [i[2] for i in task_arr]
                    data_arr = [i[1] for i in task_arr]
                    data_total = sum(data_arr)
                    cur_dis_arr = [dis[i] + diff_arr[i] for i in range(len(diff_arr))]
                    tf = Transfer(v_arr, data_total, cur_dis_arr, total_ability)
                    data_after = tf.data_tf()
                    # Calculate the utility of a single task
                    ul_uav_arr = []
                    ul = UtilityCoalition(l_idy, h_idy, task_arr, total_ability, dis, alpha_arr, final_b_arr, a, zeta)
                    for k in range(len(task_arr)):
                        u = ul.utility_single(k)
                        if len_subset_arr[k] == 0:
                            ul_uav_arr.append(0)
                            continue
                        ul_uav = u / len_subset_arr[k]
                        ul_uav_arr.append(ul_uav)
                    arr_single1.append(ul_uav_arr)
                if i == 1:
                    dis_h_before = dis_be.random_partition(lam_arr, uav_arr)
                    l_idy = [i for i in range(len(task_arr))]
                    h_idy = []
                    form = FormCoalition(dis_before, task_arr, l_idy, h_idy, total_ability, alpha_arr, b_arr_copy, a,
                                         zeta, b_total)
                    result, final_b_arr = form.form_coalition_selfish(dis_h_before)
                    ul_uav_arr = []
                    dis = []
                    ul = UtilityCoalition(l_idy, h_idy, task_arr, total_ability, dis, alpha_arr, final_b_arr, a, zeta)
                    for k in range(len(task_arr)):
                        if len(result[k]) == 0:
                            ul_uav_arr.append(0)
                            continue
                        u = ul.utility_single_Ht(k, result)
                        ul_uav = u / len(result[k])
                        ul_uav_arr.append(ul_uav)
                    arr_single2.append(ul_uav_arr)
                if i == 2:
                    dis_h_before = dis_be.random_partition(lam_arr, uav_arr)
                    l_idy = [i for i in range(len(task_arr))]
                    h_idy = []
                    form = FormCoalition(dis_h_before, task_arr, l_idy, h_idy, total_ability, alpha_arr, b_arr_copy, a,
                                         zeta, b_total)
                    result, final_b_arr = form.form_coalition_pareto(dis_h_before)
                    ul_uav_arr = []
                    dis = []
                    ul = UtilityCoalition(l_idy, h_idy, task_arr, total_ability, dis, alpha_arr, final_b_arr, a, zeta)
                    for k in range(len(task_arr)):
                        if len(result[k]) == 0:
                            ul_uav_arr.append(0)
                            continue
                        u = ul.utility_single_Ht(k, result)
                        ul_uav = u / len(result[k])
                        ul_uav_arr.append(ul_uav)
                    arr_single3.append(ul_uav_arr)
                if i == 3:
                    l_idy = [i for i in range(len(task_arr))]
                    h_idy = []
                    form = FormCoalition(dis_before, task_arr, l_idy, h_idy, total_ability, alpha_arr, b_arr_copy, a,
                                         zeta, b_total)
                    dis = form.form_non_optimization()
                    print('dis', dis)
                    from Iconversion import HeterogeneousTrans
                    h_trans = HeterogeneousTrans()
                    diff_arr = []
                    len_subset_arr = []
                    for p in range(len(dis)):
                        if p == 0:
                            nums = [j[1] for j in uav_arr]
                        subset, diff, nums = h_trans.find_subset(nums, dis[p])
                        len_subset_arr.append(len(subset))
                        diff_arr.append(diff)
                    from Transfer import Transfer
                    v_arr = [i[2] for i in task_arr]
                    data_arr = [i[1] for i in task_arr]
                    data_total = sum(data_arr)
                    cur_dis_arr = [dis[i] + diff_arr[i] for i in range(len(diff_arr))]
                    tf = Transfer(v_arr, data_total, cur_dis_arr, total_ability)
                    data_after = tf.data_tf()
                    ul_uav_arr = []
                    ul = UtilityCoalition(l_idy, h_idy, task_arr, total_ability, dis, alpha_arr, b_arr_copy, a, zeta)
                    for k in range(len(task_arr)):
                        u = ul.utility_single(k)
                        if len_subset_arr[k] == 0:
                            ul_uav_arr.append(0)
                            continue
                        ul_uav = u / len_subset_arr[k]
                        ul_uav_arr.append(ul_uav)
                    arr_single4.append(ul_uav_arr)

        avg1 = []
        avg2 = []
        avg3 = []
        avg4 = []
        for i in range(ToolHelper.task_num[work_level]):
            t1 = 0
            t2 = 0
            t3 = 0
            t4 = 0
            for j in range(ToolHelper.iter_avg):
                t1 += arr_single1[j][i]
                t2 += arr_single2[j][i]
                t3 += arr_single3[j][i]
                t4 += arr_single4[j][i]
            avg1.append(t1 / ToolHelper.iter_avg)
            avg2.append(t2 / ToolHelper.iter_avg)
            avg3.append(t3 / ToolHelper.iter_avg)
            avg4.append(t4 / ToolHelper.iter_avg)
        print(work_level)
        print('avg1', sum(avg1))
        print('avg2', sum(avg2))
        print('avg3', sum(avg3))
        print('avg4', sum(avg4))

# Reset the number of strong and weak tasks, at this time the number of strong and weak tasks is equal, and the rest remain unchanged
def experiment2_VRT():
    for work_level in ['strong', 'weak']:
        for x in [14]:
            arr_single1 = []
            arr_single2 = []
            arr_single3 = []
            arr_single4 = []
            from ToolHelper import ToolHelper
            ToolHelper = ToolHelper(0, 0)
            for m in range(ToolHelper.iter_avg):
                b_total = randint(ToolHelper.b_total[work_level][0], ToolHelper.b_total[work_level][1])
                a = randint(ToolHelper.a[0], ToolHelper.a[1])
                zeta = uniform(ToolHelper.zeta[0], ToolHelper.zeta[1])
                uav_array = []
                uav_num = 18
                for i in range(0, uav_num):
                    ability = randint(ToolHelper.ability[work_level][0],
                                      ToolHelper.ability[work_level][1])
                    from UAV import UAV
                    uav = UAV(i, ability)
                    uav_array.append(uav.store())
                total_ability = 0
                for i in range(len(uav_array)):
                    total_ability += uav_array[i][1]
                b_arr = ToolHelper.random_partition(b_total, x)

                task_arr = []
                for i in range(0, x):
                    data = randint(ToolHelper.data[work_level][0], ToolHelper.data[work_level][1])
                    from Task import Task
                    task = Task(i, data, data * ToolHelper.value_coefficient, a, zeta)
                    task_arr.append(task.store(b_arr, total_ability))
                from ToolHelper import ToolHelper
                tool = ToolHelper(task_arr, total_ability)
                dis_ini = tool.distribution_initial()
                alpha_arr = tool.alpha_arr()
                dis_abilities = DistributionAbilities(task_arr, dis_ini, total_ability)
                dis_before = dis_abilities.dis_before()
                lam_arr = tool.lam_arr()
                ballo = BandwidthAllocation(dis_before, alpha_arr, task_arr, total_ability, a, b_total, zeta)
                print('第几轮', m)
                for i in range(4):
                    b_arr_copy = b_arr.copy()
                    if i == 0:
                        new_b_arr = ballo.result(b_arr_copy)[1]
                        l_idy = [i for i in range(len(task_arr))]
                        h_idy = []
                        form = FormCoalition(dis_before, task_arr, l_idy, h_idy, total_ability, alpha_arr,
                                             new_b_arr, a, zeta, b_total)
                        dis, final_b_arr = form.form_coalition()
                        print('dis', dis)
                        from Iconversion import HeterogeneousTrans

                        h_trans = HeterogeneousTrans()
                        diff_arr = []
                        len_subset_arr = []
                        for p in range(len(dis)):
                            if p == 0:
                                nums = [j[1] for j in uav_array]
                            subset, diff, nums = h_trans.find_subset(nums, dis[p])
                            len_subset_arr.append(len(subset))
                            diff_arr.append(diff)
                        from Transfer import Transfer

                        v_arr = [i[2] for i in task_arr]
                        data_arr = [i[1] for i in task_arr]
                        data_total = sum(data_arr)
                        cur_dis_arr = [dis[i] + diff_arr[i] for i in range(len(diff_arr))]
                        tf = Transfer(v_arr, data_total, cur_dis_arr, total_ability)
                        data_after = tf.data_tf()
                        ul_uav_arr = []
                        ul = UtilityCoalition(l_idy, h_idy, task_arr, total_ability, dis, alpha_arr, final_b_arr, a,
                                              zeta)
                        for k in range(len(task_arr)):
                            u = ul.utility_single(k)
                            if len_subset_arr[k] == 0:
                                ul_uav_arr.append(0)
                                continue
                            ul_uav = u / len_subset_arr[k]
                            ul_uav_arr.append(ul_uav)
                        arr_single1.append(ul_uav_arr)
                    if i == 1:
                        ToolHelper = ToolHelper(0, 0)
                        dis_h_before = dis_abilities.random_partition(lam_arr, uav_array)
                        l_idy = [i for i in range(len(task_arr))]
                        h_idy = []
                        form = FormCoalition(dis_before, task_arr, l_idy, h_idy, total_ability, alpha_arr, b_arr_copy,
                                             a, zeta, b_total)
                        result, final_b_arr = form.form_coalition_selfish(dis_h_before)
                        ul_uav_arr = []
                        dis = []
                        ul = UtilityCoalition(l_idy, h_idy, task_arr, total_ability, dis, alpha_arr, final_b_arr, a, zeta)
                        for k in range(len(task_arr)):
                            if len(result[k]) == 0:
                                ul_uav_arr.append(0)
                                continue
                            u = ul.utility_single_Ht(k, result)
                            ul_uav = u / len(result[k])
                            ul_uav_arr.append(ul_uav)
                        arr_single2.append(ul_uav_arr)
                    if i == 2:
                        dis_h_before = dis_abilities.random_partition(lam_arr, uav_array)
                        l_idy = [i for i in range(len(task_arr))]
                        h_idy = []
                        form = FormCoalition(dis_before, task_arr, l_idy, h_idy, total_ability, alpha_arr, b_arr_copy,
                                             a, zeta, b_total)
                        result, final_b_arr = form.form_coalition_pareto(dis_h_before)
                        ul_uav_arr = []
                        dis = []
                        ul = UtilityCoalition(l_idy, h_idy, task_arr, total_ability, dis, alpha_arr, final_b_arr, a, zeta)
                        for k in range(len(task_arr)):
                            if len(result[k]) == 0:
                                ul_uav_arr.append(0)
                                continue
                            u = ul.utility_single_Ht(k, result)
                            ul_uav = u / len(result[k])
                            ul_uav_arr.append(ul_uav)
                        arr_single3.append(ul_uav_arr)
                    if i == 3:
                        l_idy = [i for i in range(len(task_arr))]
                        h_idy = []
                        form = FormCoalition(dis_before, task_arr, l_idy, h_idy, total_ability, alpha_arr, b_arr_copy,
                                             a, zeta, b_total)
                        dis = form.form_non_optimization()
                        print('dis', dis)
                        from Iconversion import HeterogeneousTrans

                        h_trans = HeterogeneousTrans()
                        diff_arr = []
                        len_subset_arr = []
                        for p in range(len(dis)):
                            if p == 0:
                                nums = [j[1] for j in uav_array]
                            subset, diff, nums = h_trans.find_subset(nums, dis[p])
                            len_subset_arr.append(len(subset))
                            diff_arr.append(diff)
                        from Transfer import Transfer

                        v_arr = [i[2] for i in task_arr]
                        data_arr = [i[1] for i in task_arr]
                        data_total = sum(data_arr)
                        cur_dis_arr = [dis[i] + diff_arr[i] for i in range(len(diff_arr))]
                        tf = Transfer(v_arr, data_total, cur_dis_arr, total_ability)
                        data_after = tf.data_tf()
                        ul_uav_arr = []
                        ul = UtilityCoalition(l_idy, h_idy, task_arr, total_ability, dis, alpha_arr, b_arr_copy, a, zeta)
                        for k in range(len(task_arr)):
                            u = ul.utility_single(k)
                            if len_subset_arr[k] == 0:
                                ul_uav_arr.append(0)
                                continue
                            ul_uav = u / len_subset_arr[k]
                            ul_uav_arr.append(ul_uav)
                        arr_single4.append(ul_uav_arr)

            vr_arr1 = []
            vr_arr2 = []
            vr_arr3 = []
            vr_arr4 = []
            for h in range(ToolHelper.iter_avg):
                variance = ToolHelper.calculate_variance(arr_single1[h])
                vr_arr1.append(variance)
                variance = ToolHelper.calculate_variance(arr_single2[h])
                vr_arr2.append(variance)
                variance = ToolHelper.calculate_variance(arr_single3[h])
                vr_arr3.append(variance)
                variance = ToolHelper.calculate_variance(arr_single4[h])
                vr_arr4.append(variance)
            vr1 = sum(vr_arr1) / len(vr_arr1)
            vr2 = sum(vr_arr2) / len(vr_arr2)
            vr3 = sum(vr_arr3) / len(vr_arr3)
            vr4 = sum(vr_arr4) / len(vr_arr4)
            print('vr1', vr1)
            print('vr2', vr2)
            print('vr3', vr3)
            print('vr4', vr4)

# experiment 3
# Reset the number of strong and weak UAVs, at this time the number of strong and weak UAVs is equal, the rest does not change
def experiment3_VRU():
    for work_level in ['strong', 'weak']:
        for x in range(4, 16):
            arr_single1 = []
            arr_single2 = []
            arr_single3 = []
            arr_single4 = []
            from ToolHelper import ToolHelper
            ToolHelper = ToolHelper(0, 0)
            for m in range(ToolHelper.iter_avg):
                b_total = randint(ToolHelper.b_total[work_level][0], ToolHelper.b_total[work_level][1])
                a = randint(ToolHelper.a[0], ToolHelper.a[1])
                zeta = uniform(ToolHelper.zeta[0], ToolHelper.zeta[1])
                uav_array = []
                uav_num = 18
                for i in range(0, uav_num):
                    ability = randint(ToolHelper.ability[work_level][0],
                                      ToolHelper.ability[work_level][1])
                    from UAV import UAV

                    uav = UAV(i, ability)
                    uav_array.append(uav.store())
                total_ability = 0
                for i in range(len(uav_array)):
                    total_ability += uav_array[i][1]
                b_arr = ToolHelper.random_partition(b_total, x)

                task_arr = []
                for i in range(0, x):
                    data = randint(ToolHelper.data[work_level][0], ToolHelper.data[work_level][1])
                    from Task import Task

                    task = Task(i, data, data * ToolHelper.value_coefficient, a, zeta)
                    task_arr.append(task.store(b_arr, total_ability))
                from ToolHelper import ToolHelper

                tool = ToolHelper(task_arr, total_ability)
                dis_ini = tool.distribution_initial()
                alpha_arr = tool.alpha_arr()
                dis_abilities = DistributionAbilities(task_arr, dis_ini, total_ability)
                dis_before = dis_abilities.dis_before()
                lam_arr = tool.lam_arr()
                ballo = BandwidthAllocation(dis_before, alpha_arr, task_arr, total_ability, a, b_total, zeta)
                for i in range(4):
                    b_arr_copy = b_arr.copy()
                    if i == 0:
                        new_b_arr = ballo.result(b_arr_copy)[1]
                        l_idy = [i for i in range(len(task_arr))]
                        h_idy = []
                        form = FormCoalition(dis_before, task_arr, l_idy, h_idy, total_ability, alpha_arr,
                                             new_b_arr, a, zeta, b_total)
                        dis, final_b_arr = form.form_coalition()
                        from Iconversion import HeterogeneousTrans

                        h_trans = HeterogeneousTrans()
                        diff_arr = []
                        len_subset_arr = []
                        for p in range(len(dis)):
                            if p == 0:
                                nums = [j[1] for j in uav_array]
                            subset, diff, nums = h_trans.find_subset(nums, dis[p])
                            len_subset_arr.append(len(subset))
                            diff_arr.append(diff)
                        from Transfer import Transfer

                        v_arr = [i[2] for i in task_arr]
                        data_arr = [i[1] for i in task_arr]
                        data_total = sum(data_arr)
                        cur_dis_arr = [dis[i] + diff_arr[i] for i in range(len(diff_arr))]
                        tf = Transfer(v_arr, data_total, cur_dis_arr, total_ability)
                        data_after = tf.data_tf()
                        ul_uav_arr = []
                        ul = UtilityCoalition(l_idy, h_idy, task_arr, total_ability, dis, alpha_arr, final_b_arr, a,
                                              zeta)
                        for k in range(len(task_arr)):
                            u = ul.utility_single(k)
                            if len_subset_arr[k] == 0:
                                ul_uav_arr.append(0)
                                continue
                            ul_uav = u / len_subset_arr[k]
                            ul_uav_arr.append(ul_uav)
                        arr_single1.append(ul_uav_arr)
                    if i == 1:
                        ToolHelper = ToolHelper(0, 0)
                        dis_h_before = dis_abilities.random_partition(lam_arr, uav_array)
                        l_idy = [i for i in range(len(task_arr))]
                        h_idy = []
                        form = FormCoalition(dis_before, task_arr, l_idy, h_idy, total_ability, alpha_arr, b_arr_copy,
                                             a, zeta, b_total)
                        result, final_b_arr = form.form_coalition_selfish(dis_h_before)
                        ul_uav_arr = []
                        dis = []
                        ul = UtilityCoalition(l_idy, h_idy, task_arr, total_ability, dis, alpha_arr, final_b_arr, a,
                                              zeta)
                        for k in range(len(task_arr)):
                            if len(result[k]) == 0:
                                ul_uav_arr.append(0)
                                continue
                            u = ul.utility_single_Ht(k, result)
                            ul_uav = u / len(result[k])
                            ul_uav_arr.append(ul_uav)
                        arr_single2.append(ul_uav_arr)
                    if i == 2:
                        dis_h_before = dis_abilities.random_partition(lam_arr, uav_array)
                        l_idy = [i for i in range(len(task_arr))]
                        h_idy = []
                        form = FormCoalition(dis_before, task_arr, l_idy, h_idy, total_ability, alpha_arr, b_arr_copy,
                                             a, zeta, b_total)
                        result, final_b_arr = form.form_coalition_pareto(dis_h_before)
                        ul_uav_arr = []
                        dis = []
                        ul = UtilityCoalition(l_idy, h_idy, task_arr, total_ability, dis, alpha_arr, final_b_arr, a,
                                              zeta)
                        for k in range(len(task_arr)):
                            if len(result[k]) == 0:
                                ul_uav_arr.append(0)
                                continue
                            u = ul.utility_single_Ht(k, result)
                            ul_uav = u / len(result[k])
                            ul_uav_arr.append(ul_uav)
                        arr_single3.append(ul_uav_arr)
                    if i == 3:
                        l_idy = [i for i in range(len(task_arr))]
                        h_idy = []
                        form = FormCoalition(dis_before, task_arr, l_idy, h_idy, total_ability, alpha_arr, b_arr_copy,
                                             a, zeta, b_total)
                        dis = form.form_non_optimization()
                        from Iconversion import HeterogeneousTrans

                        h_trans = HeterogeneousTrans()
                        diff_arr = []
                        len_subset_arr = []
                        for p in range(len(dis)):
                            if p == 0:
                                nums = [j[1] for j in uav_array]
                            subset, diff, nums = h_trans.find_subset(nums, dis[p])
                            len_subset_arr.append(len(subset))
                            diff_arr.append(diff)
                        from Transfer import Transfer

                        v_arr = [i[2] for i in task_arr]
                        data_arr = [i[1] for i in task_arr]
                        data_total = sum(data_arr)
                        cur_dis_arr = [dis[i] + diff_arr[i] for i in range(len(diff_arr))]
                        tf = Transfer(v_arr, data_total, cur_dis_arr, total_ability)
                        data_after = tf.data_tf()
                        ul_uav_arr = []
                        ul = UtilityCoalition(l_idy, h_idy, task_arr, total_ability, dis, alpha_arr, b_arr_copy, a,
                                              zeta)
                        for k in range(len(task_arr)):
                            u = ul.utility_single(k)
                            if len_subset_arr[k] == 0:
                                ul_uav_arr.append(0)
                                continue
                            ul_uav = u / len_subset_arr[k]
                            ul_uav_arr.append(ul_uav)
                        arr_single4.append(ul_uav_arr)
            vr_arr1 = []
            vr_arr2 = []
            vr_arr3 = []
            vr_arr4 = []
            for h in range(ToolHelper.iter_avg):
                variance = ToolHelper.calculate_variance(arr_single1[h])
                vr_arr1.append(variance)
                variance = ToolHelper.calculate_variance(arr_single2[h])
                vr_arr2.append(variance)
                variance = ToolHelper.calculate_variance(arr_single3[h])
                vr_arr3.append(variance)
                variance = ToolHelper.calculate_variance(arr_single4[h])
                vr_arr4.append(variance)
            vr1 = sum(vr_arr1) / len(vr_arr1)
            vr2 = sum(vr_arr2) / len(vr_arr2)
            vr3 = sum(vr_arr3) / len(vr_arr3)
            vr4 = sum(vr_arr4) / len(vr_arr4)
            print('vr1', vr1)
            print('vr2', vr2)
            print('vr3', vr3)
            print('vr4', vr4)


# Change the number of tasks;Reset the number of strong and weak tasks, at this time the number of strong and weak tasks is equal, and the rest remain unchanged
def experiment4_SAUT():
    for work_level in ['strong', 'weak']:
        # The number of tasks
        for x in range(2, 14):
            # The four algorithms arr_single store m arrays, each of which stores the utility value of each task
            arr_single1 = []
            arr_single2 = []
            arr_single3 = []
            arr_single4 = []
            from ToolHelper import ToolHelper
            ToolHelper = ToolHelper(0, 0)
            for m in range(ToolHelper.iter_avg):
                b_total = randint(ToolHelper.b_total[work_level][0], ToolHelper.b_total[work_level][1])
                a = randint(ToolHelper.a[0], ToolHelper.a[1])
                zeta = uniform(ToolHelper.zeta[0], ToolHelper.zeta[1])
                uav_array = []
                uav_num = 18
                for i in range(0, uav_num):
                    ability = randint(ToolHelper.ability[work_level][0],
                                      ToolHelper.ability[work_level][1])
                    from UAV import UAV
                    uav = UAV(i, ability)
                    uav_array.append(uav.store())
                total_ability = 0
                for i in range(len(uav_array)):
                    total_ability += uav_array[i][1]
                b_arr = ToolHelper.random_partition(b_total, x)

                task_arr = []
                for i in range(0, x):
                    data = randint(ToolHelper.data[work_level][0], ToolHelper.data[work_level][1])
                    from Task import Task
                    task = Task(i, data, data * ToolHelper.value_coefficient, a, zeta)
                    task_arr.append(task.store(b_arr, total_ability))
                from ToolHelper import ToolHelper
                tool = ToolHelper(task_arr, total_ability)
                dis_ini = tool.distribution_initial()
                alpha_arr = tool.alpha_arr()
                dis_abilities = DistributionAbilities(task_arr, dis_ini, total_ability)
                dis_before = dis_abilities.dis_before()
                lam_arr = tool.lam_arr()
                ballo = BandwidthAllocation(dis_before, alpha_arr, task_arr, total_ability, a, b_total, zeta)
                for i in range(4):
                    b_arr_copy = b_arr.copy()
                    if i == 0:
                        new_b_arr = ballo.result(b_arr_copy)[1]
                        l_idy = [i for i in range(len(task_arr))]
                        h_idy = []
                        form = FormCoalition(dis_before, task_arr, l_idy, h_idy, total_ability, alpha_arr,
                                             new_b_arr, a, zeta, b_total)
                        dis, final_b_arr = form.form_coalition()
                        from Iconversion import HeterogeneousTrans

                        h_trans = HeterogeneousTrans()
                        diff_arr = []
                        len_subset_arr = []
                        for p in range(len(dis)):
                            if p == 0:
                                nums = [j[1] for j in uav_array]
                            subset, diff, nums = h_trans.find_subset(nums, dis[p])
                            len_subset_arr.append(len(subset))
                            diff_arr.append(diff)
                        from Transfer import Transfer

                        v_arr = [i[2] for i in task_arr]
                        data_arr = [i[1] for i in task_arr]
                        data_total = sum(data_arr)
                        cur_dis_arr = [dis[i] + diff_arr[i] for i in range(len(diff_arr))]
                        tf = Transfer(v_arr, data_total, cur_dis_arr, total_ability)
                        data_after = tf.data_tf()
                        ul_uav_arr = []
                        ul = UtilityCoalition(l_idy, h_idy, task_arr, total_ability, dis, alpha_arr, final_b_arr, a,
                                              zeta)
                        for k in range(len(task_arr)):
                            u = ul.utility_single(k)
                            if len_subset_arr[k] == 0:
                                ul_uav_arr.append(0)
                                continue
                            ul_uav = u / len_subset_arr[k]
                            ul_uav_arr.append(ul_uav)
                        arr_single1.append(ul_uav_arr)
                    if i == 1:
                        ToolHelper = ToolHelper(0, 0)
                        dis_h_before = dis_abilities.random_partition(lam_arr, uav_array)
                        l_idy = [i for i in range(len(task_arr))]
                        h_idy = []
                        form = FormCoalition(dis_before, task_arr, l_idy, h_idy, total_ability, alpha_arr, b_arr_copy,
                                             a, zeta, b_total)
                        result, final_b_arr = form.form_coalition_selfish(dis_h_before)
                        ul_uav_arr = []
                        dis = []
                        ul = UtilityCoalition(l_idy, h_idy, task_arr, total_ability, dis, alpha_arr, final_b_arr, a,
                                              zeta)
                        for k in range(len(task_arr)):
                            if len(result[k]) == 0:
                                ul_uav_arr.append(0)
                                continue
                            u = ul.utility_single_Ht(k, result)
                            ul_uav = u / len(result[k])
                            ul_uav_arr.append(ul_uav)
                        arr_single2.append(ul_uav_arr)
                    if i == 2:
                        dis_h_before = dis_abilities.random_partition(lam_arr, uav_array)
                        l_idy = [i for i in range(len(task_arr))]
                        h_idy = []
                        form = FormCoalition(dis_before, task_arr, l_idy, h_idy, total_ability, alpha_arr, b_arr_copy,
                                             a, zeta, b_total)
                        result, final_b_arr = form.form_coalition_pareto(dis_h_before)
                        ul_uav_arr = []
                        dis = []
                        ul = UtilityCoalition(l_idy, h_idy, task_arr, total_ability, dis, alpha_arr, final_b_arr, a,
                                              zeta)
                        for k in range(len(task_arr)):
                            if len(result[k]) == 0:
                                ul_uav_arr.append(0)
                                continue
                            u = ul.utility_single_Ht(k, result)
                            ul_uav = u / len(result[k])
                            ul_uav_arr.append(ul_uav)
                        arr_single3.append(ul_uav_arr)
                    if i == 3:
                        l_idy = [i for i in range(len(task_arr))]
                        h_idy = []
                        form = FormCoalition(dis_before, task_arr, l_idy, h_idy, total_ability, alpha_arr, b_arr_copy,
                                             a, zeta, b_total)
                        dis = form.form_non_optimization()
                        from Iconversion import HeterogeneousTrans

                        h_trans = HeterogeneousTrans()
                        diff_arr = []
                        len_subset_arr = []
                        for p in range(len(dis)):
                            if p == 0:
                                nums = [j[1] for j in uav_array]
                            subset, diff, nums = h_trans.find_subset(nums, dis[p])
                            len_subset_arr.append(len(subset))
                            diff_arr.append(diff)
                        from Transfer import Transfer

                        v_arr = [i[2] for i in task_arr]
                        data_arr = [i[1] for i in task_arr]
                        data_total = sum(data_arr)
                        cur_dis_arr = [dis[i] + diff_arr[i] for i in range(len(diff_arr))]
                        tf = Transfer(v_arr, data_total, cur_dis_arr, total_ability)
                        data_after = tf.data_tf()
                        ul_uav_arr = []
                        ul = UtilityCoalition(l_idy, h_idy, task_arr, total_ability, dis, alpha_arr, b_arr_copy, a,
                                              zeta)
                        for k in range(len(task_arr)):
                            u = ul.utility_single(k)
                            if len_subset_arr[k] == 0:
                                ul_uav_arr.append(0)
                                continue
                            ul_uav = u / len_subset_arr[k]
                            ul_uav_arr.append(ul_uav)
                        arr_single4.append(ul_uav_arr)

            avg1 = []
            avg2 = []
            avg3 = []
            avg4 = []
            for i in range(x // 2):
                t1 = 0
                t2 = 0
                t3 = 0
                t4 = 0
                for j in range(ToolHelper.iter_avg):
                    t1 += arr_single1[j][i]
                    t2 += arr_single2[j][i]
                    t3 += arr_single3[j][i]
                    t4 += arr_single4[j][i]
                avg1.append(t1 / ToolHelper.iter_avg)
                avg2.append(t2 / ToolHelper.iter_avg)
                avg3.append(t3 / ToolHelper.iter_avg)
                avg4.append(t4 / ToolHelper.iter_avg)
            print('1strong', sum(avg1[: x // 2]))
            print('2strong', sum(avg2[: x // 2]))
            print('3strong', sum(avg3[: x // 2]))
            print('4strong', sum(avg4[: x // 2]))
            # weak
            avg1 = []
            avg2 = []
            avg3 = []
            avg4 = []
            for i in range(x // 2, x):
                t1 = 0
                t2 = 0
                t3 = 0
                t4 = 0
                for j in range(ToolHelper.iter_avg):
                    t1 += arr_single1[j][i]
                    t2 += arr_single2[j][i]
                    t3 += arr_single3[j][i]
                    t4 += arr_single4[j][i]
                avg1.append(t1 / ToolHelper.iter_avg)
                avg2.append(t2 / ToolHelper.iter_avg)
                avg3.append(t3 / ToolHelper.iter_avg)
                avg4.append(t4 / ToolHelper.iter_avg)
            print('1weak', sum(avg1[x // 2: x]))
            print('2weak', sum(avg2[x // 2: x]))
            print('3weak', sum(avg3[x // 2: x]))
            print('4weak', sum(avg4[x // 2: x]))

def experiment5_SAUU():
    # 改变无人机个数
    # Reset the number of strong and weak UAVs, at this time the number of strong and weak UAVs is equal, the rest does not change
    for work_level in ['strong', 'weak']:
        # Number of UAVs
        for x in range(4, 16):
            arr_single1 = []
            arr_single2 = []
            arr_single3 = []
            arr_single4 = []
            from ToolHelper import ToolHelper
            ToolHelper = ToolHelper(0, 0)
            for m in range(ToolHelper.iter_avg):
                b_total = randint(ToolHelper.b_total[work_level][0], ToolHelper.b_total[work_level][1])
                a = randint(ToolHelper.a[0], ToolHelper.a[1])
                zeta = uniform(ToolHelper.zeta[0], ToolHelper.zeta[1])
                uav_array = []
                uav_num = 18
                for i in range(0, uav_num):
                    ability = randint(ToolHelper.ability[work_level][0],
                                      ToolHelper.ability[work_level][1])
                    from UAV import UAV

                    uav = UAV(i, ability)
                    uav_array.append(uav.store())
                total_ability = 0
                for i in range(len(uav_array)):
                    total_ability += uav_array[i][1]
                b_arr = ToolHelper.random_partition(b_total, x)

                task_arr = []
                for i in range(0, x):
                    data = randint(ToolHelper.data[work_level][0], ToolHelper.data[work_level][1])
                    from Task import Task

                    task = Task(i, data, data * ToolHelper.value_coefficient, a, zeta)
                    task_arr.append(task.store(b_arr, total_ability))
                from ToolHelper import ToolHelper

                tool = ToolHelper(task_arr, total_ability)
                dis_ini = tool.distribution_initial()
                alpha_arr = tool.alpha_arr()
                dis_abilities = DistributionAbilities(task_arr, dis_ini, total_ability)
                dis_before = dis_abilities.dis_before()
                lam_arr = tool.lam_arr()
                ballo = BandwidthAllocation(dis_before, alpha_arr, task_arr, total_ability, a, b_total, zeta)
                for i in range(4):
                    b_arr_copy = b_arr.copy()
                    if i == 0:
                        new_b_arr = ballo.result(b_arr_copy)[1]
                        l_idy = [i for i in range(len(task_arr))]
                        h_idy = []
                        form = FormCoalition(dis_before, task_arr, l_idy, h_idy, total_ability, alpha_arr,
                                             new_b_arr, a, zeta, b_total)
                        dis, final_b_arr = form.form_coalition()
                        from Iconversion import HeterogeneousTrans
                        h_trans = HeterogeneousTrans()
                        diff_arr = []
                        len_subset_arr = []
                        for p in range(len(dis)):
                            if p == 0:
                                nums = [j[1] for j in uav_array]
                            subset, diff, nums = h_trans.find_subset(nums, dis[p])
                            len_subset_arr.append(len(subset))
                            diff_arr.append(diff)
                        from Transfer import Transfer

                        v_arr = [i[2] for i in task_arr]
                        data_arr = [i[1] for i in task_arr]
                        data_total = sum(data_arr)
                        cur_dis_arr = [dis[i] + diff_arr[i] for i in range(len(diff_arr))]
                        tf = Transfer(v_arr, data_total, cur_dis_arr, total_ability)
                        data_after = tf.data_tf()
                        ul_uav_arr = []
                        ul = UtilityCoalition(l_idy, h_idy, task_arr, total_ability, dis, alpha_arr, final_b_arr, a,
                                              zeta)
                        for k in range(len(task_arr)):
                            u = ul.utility_single(k)
                            if len_subset_arr[k] == 0:
                                ul_uav_arr.append(0)
                                continue
                            ul_uav = u / len_subset_arr[k]
                            ul_uav_arr.append(ul_uav)
                        arr_single1.append(ul_uav_arr)
                    if i == 1:
                        ToolHelper = ToolHelper(0, 0)
                        dis_h_before = dis_abilities.random_partition(lam_arr, uav_array)
                        l_idy = [i for i in range(len(task_arr))]
                        h_idy = []
                        form = FormCoalition(dis_before, task_arr, l_idy, h_idy, total_ability, alpha_arr, b_arr_copy,
                                             a, zeta, b_total)
                        result, final_b_arr = form.form_coalition_selfish(dis_h_before)
                        ul_uav_arr = []
                        dis = []
                        ul = UtilityCoalition(l_idy, h_idy, task_arr, total_ability, dis, alpha_arr, final_b_arr, a,
                                              zeta)
                        for k in range(len(task_arr)):
                            if len(result[k]) == 0:
                                ul_uav_arr.append(0)
                                continue
                            u = ul.utility_single_Ht(k, result)
                            ul_uav = u / len(result[k])
                            ul_uav_arr.append(ul_uav)
                        arr_single2.append(ul_uav_arr)
                    if i == 2:
                        dis_h_before = dis_abilities.random_partition(lam_arr, uav_array)
                        l_idy = [i for i in range(len(task_arr))]
                        h_idy = []
                        form = FormCoalition(dis_before, task_arr, l_idy, h_idy, total_ability, alpha_arr, b_arr_copy,
                                             a, zeta, b_total)
                        result, final_b_arr = form.form_coalition_pareto(dis_h_before)
                        ul_uav_arr = []
                        dis = []
                        ul = UtilityCoalition(l_idy, h_idy, task_arr, total_ability, dis, alpha_arr, final_b_arr, a,
                                              zeta)
                        for k in range(len(task_arr)):
                            if len(result[k]) == 0:
                                ul_uav_arr.append(0)
                                continue
                            u = ul.utility_single_Ht(k, result)
                            ul_uav = u / len(result[k])
                            ul_uav_arr.append(ul_uav)
                        arr_single3.append(ul_uav_arr)
                    if i == 3:
                        l_idy = [i for i in range(len(task_arr))]
                        h_idy = []
                        form = FormCoalition(dis_before, task_arr, l_idy, h_idy, total_ability, alpha_arr, b_arr_copy,
                                             a, zeta, b_total)
                        dis = form.form_non_optimization()
                        from Iconversion import HeterogeneousTrans

                        h_trans = HeterogeneousTrans()
                        diff_arr = []
                        len_subset_arr = []
                        for p in range(len(dis)):
                            if p == 0:
                                nums = [j[1] for j in uav_array]
                            subset, diff, nums = h_trans.find_subset(nums, dis[p])
                            len_subset_arr.append(len(subset))
                            diff_arr.append(diff)
                        from Transfer import Transfer

                        v_arr = [i[2] for i in task_arr]
                        data_arr = [i[1] for i in task_arr]
                        data_total = sum(data_arr)
                        cur_dis_arr = [dis[i] + diff_arr[i] for i in range(len(diff_arr))]
                        tf = Transfer(v_arr, data_total, cur_dis_arr, total_ability)
                        data_after = tf.data_tf()
                        ul_uav_arr = []
                        ul = UtilityCoalition(l_idy, h_idy, task_arr, total_ability, dis, alpha_arr, b_arr_copy, a,
                                              zeta)
                        for k in range(len(task_arr)):
                            u = ul.utility_single(k)
                            if len_subset_arr[k] == 0:
                                ul_uav_arr.append(0)
                                continue
                            ul_uav = u / len_subset_arr[k]
                            ul_uav_arr.append(ul_uav)
                        arr_single4.append(ul_uav_arr)

            avg1 = []
            avg2 = []
            avg3 = []
            avg4 = []
            for i in range(ToolHelper.task_num[work_level]):
                t1 = 0
                t2 = 0
                t3 = 0
                t4 = 0
                for j in range(ToolHelper.iter_avg):
                    t1 += arr_single1[j][i]
                    t2 += arr_single2[j][i]
                    t3 += arr_single3[j][i]
                    t4 += arr_single4[j][i]
                avg1.append(t1 / ToolHelper.iter_avg)
                avg2.append(t2 / ToolHelper.iter_avg)
                avg3.append(t3 / ToolHelper.iter_avg)
                avg4.append(t4 / ToolHelper.iter_avg)
            print(work_level)
            print('1', sum(avg1))
            print('2', sum(avg2))
            print('3', sum(avg3))
            print('4', sum(avg4))
