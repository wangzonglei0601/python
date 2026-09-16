'''获取用户输入的考试分数（转成 int）
判断规则：
90 及以上：输出优秀
80‑89：输出良好
60‑79：输出及格
小于 60：输出不及格
额外考虑：输入负数的时候，打印分数输入不合法'''
from cgi import print_form

# encoding = "utf-8"
age  = int(input("请输入你的分数"))
if age < 0 or age > 100:
    print("分数不及格")
elif age <= 60:
    print("不及格")
elif age <= 79:
    print("及格")
elif age <= 89:
    print("良好")
else:
    print("优秀")