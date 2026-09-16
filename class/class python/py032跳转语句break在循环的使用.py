# s = 0
# i = 1
# while i < 10:
#     s+=i
#     if s>20:
#         print("累加的和大于20的数字是",i)
#         break
#     i +=1
print("____________________")
i = 0
while i < 3:
    user_name = input("请输入用户名")
    pwd = input("输入你的密码")
    if user_name == "wzl" and pwd == "888888":
        break
    else:
        if  i<=2:
            print("输入错误3次后锁定，当前{}次".format(i+1))
        i +=1
else:
    print("三次错误，锁定")