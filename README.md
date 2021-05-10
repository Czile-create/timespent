# 时间使用统计
一个在Linux平台上的时间使用统计小工具，使用该应用可以：
1. 统计今天以来、一周以来的电脑使用时间。
2. 统计今天以来、一周以来每个应用的使用时间。

## 使用预览
![new-version](picture/2.png)
![picture1](picture/1.png)

## 用法
`dist` 文件夹下，存有 `getWindows`, `display` 两个可执行文件，其中：第一个可执行文件是用来监听焦点窗口的名称的，该文件将每十秒钟监听以此焦点窗口的名称，并将信息写入 `~/.timespent/{}.csv` 以及 `~/.timespent/log.txt`。其中，`{}` 中的内容为某一天的时间戳。这个应用程序是用pyinstaller生成的，源代码为 `src/getWindows.py`。

而第二个程序是用来显示统计信息的，在命令行输入` ./display` 即可显示统计信息。该可执行文件将读取前述的 `~/.timespent/` 的文件，并提取信息显示。源代码为 `src/display.py`

**使用的时候，只需要将 `getWindows` 作为开机启动程序，并将 `display` 放置在用户主目录下，（getWindows正常使用下）在终端输入 `./display` 即可快速开始。**

**getWindows的快速启用：第一次使用如果不重启，可将getWindows拖入终端，在末尾输入` &`执行**

## 待实现
`display` 程序简单地显示了我们感兴趣的内容，但是未够直观。待实现：

[ok] 使用条形图来显示，

[==] 并将整个程序打包成gnome插件，

[==] 以此实现图形化操作。

## 协议
GPL3.0