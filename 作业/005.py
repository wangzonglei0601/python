"""定义函数calc_sum(n)，接收一个参数 n
函数内部计算从 1 到 n 累加的总和，用循环实现
将计算结果 return 返回
调用函数，传入n=100，打印输出结果。"""

def calc_sum(n):
    enu = 0
    for i in range(1,n+1):
        enu+=i
    return enu
print(calc_sum(100000000))
