import os
import time
import datetime

# 获取当前的焦点窗口名称
def getfocus():
    return os.popen("xprop -id $(xprop -root _NET_ACTIVE_WINDOW | cut -d ' ' -f 5) WM_CLASS").read()

# 获取主目录路径
dirt = os.environ['HOME']

# 获取今日0点的时间戳
def getname():
    return int(time.mktime(datetime.date.today().timetuple()))

# 第一次使用的初始化
if (os.path.isdir(dirt+"/.timespent") == False):
    os.system("mkdir ~/.timespent")

while (1):
    # 读入数据
    # 数据格式： [[窗口名称, 使用次数]]
    t = []
    if os.path.isfile(dirt+"/.timespent/{}.csv".format(getname())):
        with open(dirt+"/.timespent/{}.csv".format(getname()), "r") as f:
            if (f.readable()):
                t = f.read().splitlines()
    t = [(i.split(', ')) for i in t]

    # 获取焦点窗口名称
    string = getfocus()
    # 若获取到的窗口为桌面(即什么都没有获取到)
    if (len(string) > 2):
        name = string.split('"')[-2]
    else:
        name = "desktop"

    # 若今天已经使用过该程序，则使用次数+1
    flag = False
    for i in t:
        if (i[0] == name):
            i[1] = str(int(i[1]) + 1)
            flag = True
    
    # 否则，加入今天使用的该程序
    if (flag == False):
        t.append([name, 1])

    # 保存数据，保存到~/.timespent/当天的时间戳.csv
    with open(dirt+"/.timespent/{}.csv".format(getname()), "w") as f:
        for i in t:
            f.write("{}, {}\n".format(i[0], i[1]))
    
    # 保存日志
    log = open(dirt+"/.timespent/log.txt", 'a')
    log.write("{} {}\n".format(time.time(), t))
    log.close()

    # 重复
    time.sleep(10)