# for i in range(1, 6):
#     for k in range(i+1, 6):
#         print(" ", end=' ')
#     for j in range(2*i-1):
#         print("*", end=" ")
#     print()
# print("*" * 50)
# for i in range(1, 9):
#     for j in range(1, i + 1):
#         print("*", end=" ")
#     print()
# for i in range(9,0,-1):
#     for j in range(1, i + 1):
#         print("*", end=" ")
#     print()
# for i in range(1, 9):
#     for j in range(i-1, 9):
#        print(" ", end='')
#     for k in range(2*i-1):
#         print("*", end='')
#     print()
# 只用1层for，i从1到9，前5行*，后4行*倒三角
for i in range(1, 10):
    if i <= 5:
        # 上半部分：正三角 *
        line = i
        char = "*"
    else:
        # 下半部分：倒三角 *
        line = 10 - i
        char = "*"
    # 打印前置空格
    for j in range(line - 1, 6):
        print(" ", end="")
    # 打印符号
    for k in range(2 * line - 1):
        print(char, end="")
    print()