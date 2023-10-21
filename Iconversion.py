# -*- coding: utf-8 -*-
"""
@Time ： 2023-09-29 21:20
@Auth ： Huailing Ma
@File ：Iconversion.py
@IDE ：PyCharm
@Motto：ABC(Always Be Coding)
"""

class HeterogeneousTrans:
    """This class represents the assignment under the isomorphic conversion"""

    # Find the subset closest to target
    def find_subset(self, nums, target):
        # Here nums is the array of working capacity of UAV
        n = len(nums)
        total_sum = sum(nums)

        # Create a two-dimensional array dp, dp[i][j] means to select some numbers from the first i digits such that their sum equals j
        dp = [[False for _ in range(total_sum + 1)] for _ in range(n + 1)]
        dp[0][0] = True

        for i in range(1, n + 1):
            for j in range(total_sum + 1):
                dp[i][j] = dp[i - 1][j]
                if nums[i - 1] <= j:
                    dp[i][j] |= dp[i - 1][j - nums[i - 1]]

        # Create a two-dimensional array dp, dp[i][j] means to select some numbers from the first i digits such that their sum equals j
        closest_sum = 0
        if target <= total_sum:
            for j in range(target, -1, -1):
                if dp[n][j]:
                    closest_sum = j
                    break
            # Find the sum of the subsets closest to the target from back to front
            for j in range(target, 2 * target - closest_sum + 1):
                if dp[n][j]:
                    closest_sum = j
                    break
            subset = []
            i, j = n, closest_sum
            while i > 0 and j > 0:
                if not dp[i - 1][j]:
                    subset.append(nums[i - 1])
                    j -= nums[i - 1]
                    del nums[i - 1]
                i -= 1
        else:
            closest_sum = total_sum
            subset = nums.copy()
            nums = []

        return subset, closest_sum - target, nums