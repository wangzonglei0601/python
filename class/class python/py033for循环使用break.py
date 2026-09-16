# for i in "hello":
#     print(i)
#     if i =="e":
#         break
#     print(i)
# print("____________________")
# for i in range(3):
#     user_name = input("请输入用户名")
#     pwd = input("输入你的密码")
#     if user_name == "wzl" and pwd == "888888":
#         break
#     else:
#         if  i<=2:
#             print("输入错误3次后锁定，当前{}次".format(i+1))
# else:
#     print("三次错误，锁定")

# 先读文件，拿到正确的账号和密码
with open(r'C:\Users\你的用户名\Desktop\pwd.txt', 'r') as f:
    data = f.read().split()  # 把文件里的内容读出来，切成两半
    correct_user = data[0]   # 拿到账号
    correct_pwd = data[1]    # 拿到密码

for i in range(3):
    user_name = input("请输入用户名")
    pwd = input("输入你的密码")
    if user_name == correct_user and pwd == correct_pwd:
        print("登录成功！")
        break
    else:
        print(f"输入错误，当前第{i+1}次")
else:
    print("三次错误，锁定")