import os
import time
import datetime
def getfocus():
    return os.popen("xprop -id $(xprop -root _NET_ACTIVE_WINDOW | cut -d ' ' -f 5) WM_CLASS").read()

dirt = os.environ['HOME']
def getname():
    return int(time.mktime(datetime.date.today().timetuple()))

if (os.path.isdir(dirt+"/.timespent") == False):
    os.system("mkdir ~/.timespent")

while (1):
    t = []
    if os.path.isfile(dirt+"/.timespent/{}.csv".format(getname())):
        with open(dirt+"/.timespent/{}.csv".format(getname()), "r") as f:
            if (f.readable()):
                t = f.read().splitlines()
    t = [(i.split(', ')) for i in t]
    string = getfocus()
    if (len(string) > 2):
        name = string.split('"')[-2]
    else:
        name = "desktop"
    flag = False
    for i in t:
        if (i[0] == name):
            i[1] = str(int(i[1]) + 1)
            flag = True
    if (flag == False):
        t.append([name, 1])
    with open(dirt+"/.timespent/{}.csv".format(getname()), "w") as f:
        for i in t:
            f.write("{}, {}\n".format(i[0], i[1]))
    log = open(dirt+"/.timespent/log.txt", 'a')
    log.write("{} {}\n".format(time.time(), t))
    log.close()
    time.sleep(10)