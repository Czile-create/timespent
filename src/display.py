import os
import time, datetime

# 获取当天的时间戳
def getname():
    return int(time.mktime(datetime.date.today().timetuple()))

# 获取一周的时间戳
def getweektime():
    ans = []
    today = datetime.date.today()
    for i in range(7):
        ans.append(int(time.mktime((today - datetime.timedelta(days=i)).timetuple())))
    return ans

# 返回条形图
# i: 总数
# j: 当前类别数
# maxsize: 条形图的总大小
# TODO: 报错处理：maxsize不够
def showchart(i, j, maxsize):
    maxsize = maxsize - 6
    numofequals = int(j * maxsize / i)
    return (" ( {}{} ) ".format('='*numofequals, ' '*(maxsize - numofequals)))

# 将字体颜色调成蓝色
def blue(s):
    return "\033[34m{}\033[0m".format(s)

# 将字体颜色调成蓝绿色
def blue_green(s):
    return "\033[36m{}\033[0m".format(s)

# 将字体颜色调成绿色
def green(s):
    return "\033[32m{}\033[0m".format(s)

# 将字体颜色调成白色
def white(s):
    return "\033[37m{}\033[0m".format(s)

# 显示总览条形图
def showgeneral(t, totaltime, maxsize):
    maxsize = maxsize - 6
    block = []
    for i in t[:min(3, len(t))]:
        block.append(int(int(i[1]) * maxsize/ totaltime))
    while (len(block) < 3):
        block.append(0)
    return " ( {}{}{}{} ) ".format(block[0] * green('='), block[1] * blue('='), block[2] * blue_green('='), (maxsize - sum(block)) * white('='))
    
# 读入文件数据
# 文件格式：[[programs name, using times]]
def readfile(filename):
    t = []
    if os.path.isfile(filename):
        with open(filename) as f:
            if (f.readable()):
                t = f.read().splitlines()
    return [(i.split(', ')) for i in t]

# 显示数据
# s: 提示数据
# t: 已读入的数据数组
def display(s, t):
    # 计算使用的总时间
    # 总时间 = 总使用次数 * 10秒
    totaltime = 0
    for i in t:
        totaltime += int(i[1])
    
    # 按应用使用时间从大到小排序
    t.sort(key=lambda x: int(x[1]), reverse=True)

    # 输出总览图
    print("{}{}{}{}".format(s.ljust(10), showgeneral(t, totaltime, os.get_terminal_size().columns - 10 - 16), "{}%".format(int(totaltime * 1000 / 3600 / 24)).ljust(7), str(datetime.timedelta(seconds=totaltime * 10)).rjust(9)))

    # 输出总览图注释：前三使用时间应用名称
    max3 = []
    for i in t[:min(len(t), 3)]:
        max3.append("={}    ".format(i[0]))
    while (len(max3) < 3):
        max3.append("")
    print("{}{}{}{}".format(green(max3[0]), blue(max3[1]), blue_green(max3[2]), white("=other")))

    # 输出前五个应用具体使用时间
    print("Here are the Apps you spent most of the time {}:".format(s))
    maxsize = max(len(i[0]) for i in t[:min(len(t), 5)])
    for i in t[:min(len(t), 5)]:
        print("{}{}{}{}".format(i[0].ljust(maxsize), showchart(int(t[0][1]), int(i[1]), os.get_terminal_size().columns - 16 - maxsize), "{}%".format(int(int(i[1]) * 1000 / 3600 / 24)).ljust(7), str(datetime.timedelta(seconds=int(i[1]) * 10)).rjust(9)))

# 输出今日的图表
def today(dirt):
    filename = dirt+"/.timespent/{}.csv".format(getname())
    t = readfile(filename)
    display("Today", t)

# 输出这周以来的图表
def week(dirt):
    filenames = getweektime()
    t = []
    for fn in filenames:
        filename = dirt+"/.timespent/{}.csv".format(fn)
        tmp = readfile(filename)
        for i in tmp:
            flag = True
            for j in t:
                if (j[0] == i[0]):
                    j[1] = str(int(j[1]) + int(i[1]))
                    flag = False
            if (flag == True):
                t.append(i)
    
    display("This week", t)

# 本程序实际上可以输出任意时间以来的图表
# TODO: 参数 -d 表示输出多少日以来的图表
# 本程序可以找任意时间以来的某一应用使用时间
# TODO: 参数 -p 表示某一应用的使用时间统计
dirt = os.environ['HOME']
today(dirt)
print("\n")
week(dirt)