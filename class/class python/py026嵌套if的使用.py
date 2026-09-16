answer= input("请问你喝酒了吗")
if answer  == "y":
    print("yes")
    proon = int(input("酒精测试"))
    print("测试酒精含量")
    if proon <20:
        print("小于测试含量，可以开车")
    else:
        print("抓起来")
else:
    print("no")