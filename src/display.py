import os, sys
import time, datetime
import getopt

# 获取当天的时间戳
def getname():
    return int(time.mktime(
        datetime.date.today().timetuple()
    ))

# 获取一周的时间戳
def getweektime(day=7):
    ans = []
    today = datetime.date.today()
    for i in range(day):
        ans.append(int(time.mktime((
            today - datetime.timedelta(days=day-i-1)
        ).timetuple())))
    return ans

# 返回条形图
# i: 总数
# j: 当前类别数
# maxsize: 条形图的总大小
# TODO: 报错处理：maxsize不够
def showchart(i, j, maxsize):
    maxsize = maxsize - 6
    if (i != 0):
        numofequals = int(j * maxsize / i)
    else:
        numofequals = 0
    return (" ( {}{} ) ".format(
        '='*numofequals,
        ' '*(maxsize - numofequals)
    ))

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
    return " ( {}{}{}{} ) ".format(
        block[0] * green('='), 
        block[1] * blue('='), 
        block[2] * blue_green('='), 
        (maxsize - sum(block)) * white('=')
    )
    
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
# m: 最大显示应用数
def display(s, t, m=5):
    # 计算使用的总时间
    # 总时间 = 总使用次数 * 10秒
    totaltime = 0
    for i in t:
        totaltime += int(i[1])
    
    # 按应用使用时间从大到小排序
    t.sort(key=lambda x: int(x[1]), reverse=True)

    printtime = str(datetime.timedelta(seconds=totaltime * 10))
    # 输出总览图
    print("{}{}{}{}".format(
        s.ljust(10), 
        showgeneral(
            t, 
            totaltime, 
            os.get_terminal_size().columns - 10 - 8 - len(printtime)
        ), 
        printtime, 
        "{}%".format(int(totaltime * 1000 / 3600 / 24)).rjust(7)
    ))

    if t == []:
        return

    # 输出总览图注释：前三使用时间应用名称
    max3 = []
    for i in t[:min(len(t), 3)]:
        max3.append("={}    ".format(i[0]))
    while (len(max3) < 3):
        max3.append("")
    print("{}{}{}{}".format(
        green(max3[0]), 
        blue(max3[1]), 
        blue_green(max3[2]), 
        white("=other")
    ))

    # 输出前五个应用具体使用时间
    print("Here are the Apps you spent most of the time:")
    maxsize = max(len(i[0]) for i in t[:min(len(t), m)])
    maxsizeOfPrinttime = max(
        len(str(
            datetime.timedelta(seconds=int(i[1]) * 10)
        )) for i in t[:min(len(t), m)]
    )
    for i in t[:min(len(t), m)]:
        printtime =  str(datetime.timedelta(seconds=int(i[1]) * 10))
        print("{}{}{}{}".format(
            i[0].ljust(maxsize), 
            showchart(
                int(t[0][1]), 
                int(i[1]), 
                os.get_terminal_size().columns - 8 - maxsize - maxsizeOfPrinttime
            ), 
            printtime.rjust(maxsizeOfPrinttime), 
            "{}%".format(int(int(i[1]) * 1000 / 3600 / 24)).rjust(7)
        ))

# 输出一段时间以来的图表
# dirt： 主目录
# i: 指定的天数
# m: 最大显示应用数
def inday(dirt, _i, _m):
    filenames = getweektime(day=_i)
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
    
    display("In {} days".format(_i), t, m=_m)

# 输出指定某一天的信息
# dirt: 主目录
# date: YYYY-mm-dd
# m: 最大应用显示数
def getaday(dirt, date, m):
    try:
        filename = "{}/.timespent/{}.csv".format(
            dirt, 
            int(time.mktime(time.strptime(date, "%Y-%m-%d")))
        )
    except:
        print("The format of date should be yyyy-mm-dd!")
        exit(3)
    t = readfile(filename)
    display(date, t, m)

def getProgramData(dirt, name, i):
    t = []
    datelist = getweektime(day=i)
    for filename in datelist:
        tmp = readfile("{}/.timespent/{}.csv".format(dirt, filename))
        flag = False
        for j in tmp:
            if j[0] == name:
                t.append(int(j[1]))
                flag = True
        if flag == False:
            t.append(0)
    
    tmp = "The time you spent on {} in {} days is: ".format(name, i)
    totaltime = sum([j for j in t]) * 10
    _totaltime = str(datetime.timedelta(seconds=totaltime))
    print("{}{}{}%".format(
        tmp, 
        _totaltime.rjust(
            os.get_terminal_size().columns - len(tmp) - 8
        ), 
        str(int(totaltime * 100 / 3600 / 24)).rjust(7)
    ))

    maxsize = max(j for j in t)
    for j in t:
        i -= 1
        _totaltime = str(datetime.timedelta(seconds=j * 10))
        print("Today - {}: {}{}{}%".format(
            str(i).rjust(3), 
            showchart(maxsize, j, os.get_terminal_size().columns - len(_totaltime) - 8), 
            _totaltime, 
            str(int(j * 1000/ 3600 / 24)).rjust(7), 
        ))


            

# 获取主目录
dirt = os.environ['HOME']

# 默认值
date = time.strftime("%Y-%m-%d", time.localtime(getname()))
m = 5
i = 7
p = ""

# 读取参数
try:
    opts, args = getopt.getopt(
        sys.argv[1:], 
        "d:f:gp:hi:", 
        ["day=", "from=", "program=", "in="]
    )
except:
    print("Error parameter!")
    exit(1)
if (len(args) != 0):
    print("Unused parameter")
    exit(2)

# 利用参数修改默认值
for opt, arg in opts:
    if opt == "-h":
        print('''
# Timespent
A time usage statistics tool on Linux platform, which can display:
1. Statistics of computer use time since today and in the past week.
2. Count the usage time of each application today and in the past week.

## Usage
1. Set the program `dist/getWindows` open automatically at boot
2. Move the program `dist/display` to your directory `~` (this is to say, Input `mv dist/display ~` in terminal)
3. Reboot
4. Type `./display` in terminal to start

## Parameter
[==] para `-d` : print the data of specified day
[==] para `-i` : print the data in the past several days
[==] para `-f` : print the data since specified number of days
[==] para `-g` : print all the programs instead of top 5 programs
[==] para `-p` : Only print the specified program's data
''')
        exit(4)
    elif opt == "-g":
        m = 360 * 24
    elif opt in ["-d", "--day"]:
        date = arg
    elif opt in ["-i", "--in"]:
        try:
            i = int(arg)
        except:
            print("-i Must be an integer.")
            exit(6)
    elif opt in ["-f", "--from"]:
        try:
            if "--in" in opt or "-i" in opt:
                print("Parameter Error, '-i' '-f' cannot use in the same time")
            tmp = datetime.datetime.strptime(arg, "%Y-%m-%d")
            i = (datetime.datetime.today() - tmp).days
        except:
            print("The format of date should be yyyy-mm-dd")
            exit(7)
    elif opt in ["-p", "--program"]:
        p = arg
    else:
        print("Parameter Error!")
        exit(5)

opts = [i[0] for i in opts]

flag = 0
# 输出数据
if "-p" in opts or "--program" in opts:
    getProgramData(dirt, p, i)
    print()
    flag = 1
if "-d" in opts or "--day" in opts:
    getaday(dirt, date, m)
    print()
    flag = 1
if "-i" in opts or "--in" in opts or "--from" in opts or "-f" in opts:
    inday(dirt, i, m)
    print()
    flag = 1


if (flag == 0):
    getaday(dirt, date, m)
    print()
    inday(dirt, i, m)