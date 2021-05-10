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

# TODO:
# def showgeneral(i, j, )

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
    print("{}{}{}{}".format(s.ljust(10), ' '*(os.get_terminal_size().columns - 10 - 16), "{}%".format(int(totaltime * 1000 / 3600 / 24)).ljust(7), str(datetime.timedelta(seconds=totaltime * 10)).rjust(9)))
    t.sort(key=lambda x: int(x[1]), reverse=True)
    print("Here are the Apps you spent most of the time {}:".format(s))
    maxsize = max(len(i[0]) for i in t[:min(len(t), 5)])
    for i in t[:min(len(t), 5)]:
        print("{}{}{}{}".format(i[0].ljust(maxsize), showchart(int(t[0][1]), int(i[1]), os.get_terminal_size().columns - 16 - maxsize), "{}%".format(int(int(i[1]) * 1000 / 3600 / 24)).ljust(7), str(datetime.timedelta(seconds=int(i[1]) * 10)).rjust(9)))
        # showchart(int(t[0][1]), int(i[1]))


def today(dirt):
    filename = dirt+"/.timespent/{}.csv".format(getname())
    t = readfile(filename)
    display("today", t)

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
    
    display("this week", t)

dirt = os.environ['HOME']
today(dirt)
print("\n")
week(dirt)