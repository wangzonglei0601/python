# while True:
#     s = int(input("输入分数，输入-1退出："))
#     if s == -1:
#         print("程序结束")
#         break
#     print("等级：", s)
# s = 0
# a = 1
# while a < 10:
#     print(a)
#     a += 1
i = 1
while i < 4:
    print(f'第{i}次输入')
    user = input('请输入你的用户名')
    pod = input('请输入你的密码')
    if user =='wzl'and pod == '8888':
        break
    i = i + 1
