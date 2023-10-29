from command import *
from line import *
from log import *

queue = CommandQueue()
history = History()
stats = Statistic()

history.start_session()
stats.start_session()

class Adapter(object):
    # Converts the original command into a format that can be executed directly
    def solve(input):
        history.push(input)
        history.push(input)
        input = input.split(' ')

        if (input[0] == "history"):
            if (len(input) > 1):
                history.show_num(int(input[1]))
            else:
                history.show_all()
            return

        if (input[0] == "stats"):
            if (len(input) > 1 and input[1] == "all"):
                stats.show_all()
            else:
                stats.show_current()
            return
        
        if (input[0] == "undo"):
            queue.undo()
            return
        
        if (input[0] == "redo"):
            queue.redo()
            return

        if (input[0] == "load"):
            stats.open_file()
            command = Load(input[1])
            
        
        if (input[0] == "save"):
            command = Save()
        
        if (input[0] == "insert"):
            if (input[1].isdigit()):
                command = Insert(int(input[1]), ' '.join(input[2:]))
            else:
                command = AppendTail(' '.join(input[1:]))
        
        if (input[0] == "append-head"):
            command = AppendHead(' '.join(input[1:]))
        
        if (input[0] == "append-tail"):
            command = AppendTail(' '.join(input[1:]))
        
        if (input[0] == "delete"):
            if (input[1].isdigit()):
                command = DeletePos(int(input[1]))
            else:
                command = DeleteText(input[1])
        
        if (input[0] == "list"):
            command = Show()

        if (input[0] == "list-tree"):
            command = TreeShow()

        if (input[0] == "dir-tree"):
            command = DirShow(input[1])
        
        queue.excute(command)


adapter = Adapter()


while True:
    input = input("Please input your command:")
    if (input == "quit"):
        break
    adapter.solve(input)

print("Session is over")
    