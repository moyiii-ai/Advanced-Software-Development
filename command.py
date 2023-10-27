from line import *

class Adapter(object):
    # converts the original command into a format that can be executed directly
    pass


class Command(object):
    pass


class CommandQueue(object):
    # A queue used to maintain all commands

    def __init__(self):
        self.tail = 0
        self.queue = {}

    # TODO(A): push a command in the end of queue
    def push(self):
        pass
    
    # TODO(A): execute the command
    def excute(self):
        pass

    # TODO(A): redo the last command, can call excute
    def redo(self):
        pass

    # TODO(A): undo the last command
    def undo(self):
        pass