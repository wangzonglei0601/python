#coding=utf-8
fp=open("text.txt",'w')
print('人生苦短，我用python',file=fp)
fp.close()

q=input('请输入你的姓名')
w=input('请输入你的年纪')
e=input('请输入你的座右铭')
print('姓名',q)
print('年纪',w)
print('座右铭',e)