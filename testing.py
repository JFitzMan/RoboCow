import random
input = '!roll 100D200'

s = input.split()
print(s)
nums = s[1].split('d')
if len(nums) == 1: nums = s[1].split('D')
print(nums)
dice = int(nums[1])
times = int(nums[0])
result = 0
string = ''
for x in range(0, times):
    roll = random.randint(1, dice)
    string = string+str(roll)+' + '
    result+=roll
print(string[0:-3])
print(result)

