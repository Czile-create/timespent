import os
import time, datetime

def getname():
    return int(time.mktime(datetime.date.today().timetuple()))

def getweektime():
    ans = []
    today = datetime.date.today()
    for i in range(7):
        ans.append(int(time.mktime((today - datetime.timedelta(days=i)).timetuple())))
    return ans

def showchart(i, j, maxsize):
    maxsize = maxsize - 6
    numofequals = int(j * maxsize / i)
    return (" ( {}{} ) ".format('='*numofequals, ' '*(maxsize - numofequals)))

def blue(s):
    return "\033[34m{}\033[0m".format(s)

def blue_green(s):
    return "\033[36m{}\033[0m".format(s)

def green(s):
    return "\033[32m{}\033[0m".format(s)

def white(s):
    return "\033[37m{}\033[0m".format(s)

# TODO:
def showgeneral(t, totaltime, maxsize):
    maxsize = maxsize - 6
    block = []
    for i in t[:min(3, len(t))]:
        block.append(int(int(i[1]) * maxsize/ totaltime))
    while (len(block) < 3):
        block.append(0)
    return " ( {}{}{}{} ) ".format(block[0] * green('='), block[1] * blue('='), block[2] * blue_green('='), (maxsize - sum(block)) * white('='))
    

def readfile(filename):
    t = []
    if os.path.isfile(filename):
        with open(filename) as f:
            if (f.readable()):
                t = f.read().splitlines()
    return [(i.split(', ')) for i in t]

def display(s, t):
    # TODO:
    # showgeneral()
    totaltime = 0
    for i in t:
        totaltime += int(i[1])
    t.sort(key=lambda x: int(x[1]), reverse=True)
    print("{}{}{}{}".format(s.ljust(10), showgeneral(t, totaltime, os.get_terminal_size().columns - 10 - 16), "{}%".format(int(totaltime * 1000 / 3600 / 24)).ljust(7), str(datetime.timedelta(seconds=totaltime * 10)).rjust(9)))
    max3 = []
    for i in t[:min(len(t), 3)]:
        max3.append("={}    ".format(i[0]))
    while (len(max3) < 3):
        max3.append("")
    print("{}{}{}{}".format(green(max3[0]), blue(max3[1]), blue_green(max3[2]), white("=other")))
    print("Here are the Apps you spent most of the time {}:".format(s))
    maxsize = max(len(i[0]) for i in t[:min(len(t), 5)])
    for i in t[:min(len(t), 5)]:
        print("{}{}{}{}".format(i[0].ljust(maxsize), showchart(int(t[0][1]), int(i[1]), os.get_terminal_size().columns - 16 - maxsize), "{}%".format(int(int(i[1]) * 1000 / 3600 / 24)).ljust(7), str(datetime.timedelta(seconds=int(i[1]) * 10)).rjust(9)))
        # showchart(int(t[0][1]), int(i[1]))


def today(dirt):
    filename = dirt+"/.timespent/{}.csv".format(getname())
    t = readfile(filename)
    display("Today", t)

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

# print(white("Hello World"))
dirt = os.environ['HOME']
today(dirt)
print("\n")
week(dirt)