'''Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.You may assume that each input would have exactly one solution, and you may not use the same element twice.You can return the answer in any order.
    Example1:
    Input: nums = [2,7,11,15], target = 9
    Output: [0,1]
    Explanation: Because nums[0] + nums[1] == 9, we return [0, 1].
    Constraints:
        2 <= nums.length <= 104
        -109 <= nums[i] <= 109
        -109 <= target <= 109
        Only one valid answer exists.'''
def coup_nums(nums:list, target: int)->list:
    for i in range(len(nums)):
        flag = target - nums[i];
        if flag in nums:
            return [i, nums.index(flag)]
        
if __name__ == "__main__":
    num = list(map(int, input("请输入数字,用逗号分隔").split(',')))
    target = int(input("请输入target"))
    print(coup_nums(num, target))