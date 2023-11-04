from command import *
from line import *
from log import *

def run():
    queue = CommandQueue()
    history = History()
    stats = Statistic()

    history.start_session()
    stats.start_session()

    class Adapter(object):
        # Converts the original command into a format
        # that can be executed directly #

        def solve(self, input):
            history.push(input)
            #history.push(input)
            input_0 = input.split(' ')[0]
            input_1 = input[len(input_0) + 1:]
            input = [input_0, input_1]

        # The command would be a sentence
        # split the sentence to find out the first word, which is input[0] #

            if (input[0] == "history"):
                if (len(input) > 1):
                    history.show_num(int(input[1]))
                else:
                    history.show_all()
                return
            # HISTORY command, 2 usages #
            # 01 "history x" (x is number), show x history in list #
            # 02 "history", show all history in list #

            if (input[0] == "stats"):
                if (len(input) > 1 and input[1] == "all"):
                    stats.show_all()
                else:
                    stats.show_current()
                return
            # STATS command, 2 usages #
            # 01 "stats all", show all stats in list #
            # 02 "stats", show current stats #

            if (input[0] == "undo"):
                queue.undo()
                return
            # UNDO command, 1 usage #
            # 01 "undo", just undo the last command #

            if (input[0] == "redo"):
                queue.redo()
                return
            # REDO command, 1 usage #
            # 01 "redo", just execute the last revoked command #

            if (input[0] == "load"):
                stats.open_file(input[1])
                # stats.open_file does nothing else but record the time #
                command = Load(input[1])
                # Load(input[1]) is the func to open the file #
            # LOAD command, 1 usage #
            # 01 "load PATH", open the file at PATH #
            # Hints: if file at PATH is not existed, create it #

            if (input[0] == "save"):
                command = Save()
            # SAVE command, 1 usage #
            # 01 "save", save the file which is being edited #

            if (input[0] == "insert"):
                if (input[1][0].isdigit()):
                    second = input[1].split(' ')[0]
                    third = input[1][len(second) + 1:]
                    second = int(second)
                    #command = Insert(int(input[1]), ' '.join(input[2:]))
                    command = Insert(second, third)
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
                if (len(input) > 1):
                    command = DirShow(input[1])
                else:
                    command = TreeShow()

            queue.excute(command)


    adapter = Adapter()


    while True:
        user_input = input("Please input your command:")
        if (user_input == "quit"):
            break
        # Only if the user input "quit" will the program end #
        adapter.solve(user_input)

    print("Session is over")


if __name__ == '__main__':
    run()
    
