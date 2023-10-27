from line import *

class Adapter(object):
    # converts the original command into a format that can be executed directly
    pass


class Command(object):
    pass


class CommandQueue(object):
    # A queue used to maintain all commands

    def __init__(self):
        # as we need to undo and redo, use a list to implement queue
        self.tail = 0
        self.queue = {}

    # TODO(A): push a command in the end of queue
    def push(self):
        pass
    
    # TODO(A): execute the command, call adapter
    def excute(self):
        pass

    # TODO(A): redo the last command, call excute
    def redo(self):
        pass

    # TODO(A): undo the last command
    def undo(self):
        # notice: skip the list/list-tree/dir-tree, but no load/save
        pass


class History(object):
    def __init__(self):
        self.tail = 0
        self.queue = {}

    # TODO(B): Start a new session and add a line in history
    def start(self):
        pass

    # TODO(B): Open a new file and clear the history buffer
    def open(self):
        pass
    
    # TODO(B): Insert the command to the history buffer
    def push(self, command):
        pass
    
    # TODO(B): Save the history of this session into history file
    def save(self):
        pass


class Statistic(object):
    # Record the working time of all files in the current session
    def __init__(self):
        self.tail = 0
        self.queue = {}
    
    # TODO(B): Open a new file and record the start time
    def open(self):
        pass
    
    # TODO(B): Print all working time in the queue
    def show_all(self):
        pass
    
    # TODO(B): Print the last num working time in the queue
    def show(self, num):
        pass