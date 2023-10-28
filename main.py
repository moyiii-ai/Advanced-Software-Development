from re import S
from turtle import st
from line import *
from command import *


queue = CommandQueue()
list = LineList()
history = History()
stats = Statistic()


history.start_session()
stats.start_session()


while True:
    input = input("Please input your command:")
    history.push(input)
    input = input.split(' ')

    if (input[0] == "history"):
        if (len(input) > 1):
            history.show_num(int(command[1]))
        else:
            history.show_all()
        continue

    if (input[0] == "stats"):
        if (len(input) > 1 and input[1] == "all"):
            stats.show_all()
        else:
            stats.show_current()
        continue

    if (input[0] == "load"):
        stats.open_file()
    
    command = Command(input)
    queue.exeute(command)