# 获取用户输入成绩
score = float(input("请输入你的考试成绩："))

# 多分支if判断
if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
elif score >= 60:
    grade = "D"
else:
    grade = "不及格"

# 输出结果
print(f"你的成绩等级是：{grade}")