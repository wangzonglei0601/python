#使用循环，计算 1~100 所有数字的累加总和（1+2+3+…+100）

con = 0
i = 1
for i in range(1,101):
    con += i
print(con)
while i < 100:
    con += i
    i+=1
print(con)
