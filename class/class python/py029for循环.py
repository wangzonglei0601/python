# for ii in range(1,11):
#
#     if ii%2==0:
#         print(ii)
# 遍历100~999所有三位数
for num in range(100, 1000):
    # 拆分百位、十位、个位
    a = num // 100        # 百位
    b = num // 10 % 10    # 十位
    c = num % 10          # 个位
    # 判断立方和是否等于原数
    if a**3 + b**3 + c**3 == num:
        print(num)