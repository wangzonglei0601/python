"""写循环，遍历数字 1‑5
在循环内try执行：如果 i 等于 3，执行1 / 0制造报错；其余数字打印 i
except捕获异常，打印：出现错误，跳过本条
保证程序不会崩溃，继续执行后面循环"""

for i in range(1, 5+1):
    try:
        if i ==3:
            i=1/0
            continue
        print(i)
    except ZeroDivisionError:
        print(f"第{i}出现错误，跳过本条")
