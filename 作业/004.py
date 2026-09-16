"""创建一个列表，里面存放 5 个城市名字
使用 for 循环遍历列表，逐行打印每个城市
再创建字典，保存一个学生信息：姓名、性别、年龄、爱好"""
leibian = ["上海","朝阳","喀左","北京","石家庄"]
for i in leibian:
    print(i,end=" ")
while True:
    print(leibian)
    break
xuesheng = {"姓名":"王宗磊","性别":"男","年龄":"30","爱好":"python"}
for key,value in xuesheng.items():
    print(key,":",value, end=" ")
while True:
    print(xuesheng)
    break