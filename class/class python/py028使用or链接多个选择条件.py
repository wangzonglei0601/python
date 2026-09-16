# user = input('请输入你的用户名')
# if user == 'wzl'or user == '8888':
#     print("yes")
# else:
#     print("no")
score = float(input("请输入考试成绩："))

match True:
    case _ if score < 0 or score > 100:
        grade = "成绩输入错误"
    case _ if score >= 90:
        grade = "A"
    case _ if score >= 80:
        grade = "B"
    case _ if score >= 70:
        grade = "C"
    case _ if score >= 60:
        grade = "D"
    case _:
        grade = "不及格"

print(f"你的成绩等级：{grade}")