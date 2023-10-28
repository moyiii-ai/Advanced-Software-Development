from line import *

class Adapter(object):
    # Converts the original command into a format that can be executed directly
    pass


class Command(object):
    def __init__(self, *arg):
        pass


class CommandQueue(object):
    # A queue used to maintain all commands

    def __init__(self):
        # As we need to undo and redo, use a list to implement queue
        self.tail = 0
        self.queue = {}

    # TODO(A): Execute a command by calling adapter, push it in the end of queue
    def excute(self):
        # Notice: for the load/save command, clear the queue as they can't undo
        pass

    # TODO(A): Undo the last command
    def undo(self):
        # Notice: skip the list/list-tree/dir-tree, but no load/save
        pass

    # TODO(A): Redo the last command, call excute
    def redo(self):
        # Notice: check if the last command is undo
        pass

    


class History(object):
    def __init__(self):
        self.tail = 0
        self.queue = {}

    # TODO(B): Start a new session and load the history file
    def start_session(self):
        # Don't forget to write a session line into history file!
        pass
    
    # TODO(B): Insert the command to the history buffer, and save it to file
    def push(self, command):
        pass
    
    # TODO(B): Print the last num history command
    def show_num(self, num):
        pass
    
    # Print all history command
    def show_all(self):
        self.show_num(self, self.tail)


class Statistic(object):
    # Record the working time of all files in the current session
    def __init__(self):
        self.tail = 0
        self.work_time = 0
        self.queue = {}

    # TODO(B): Start a new session, clear the queue and load the stats file    
    def start_session(self):
        # Don't forget to write a session line into stats file!
        pass

    # TODO(B): Open a new file and record the start time
    # save the working time of last file in the queue and stats file
    def open_file(self):
        pass
    
    # TODO(B): Print all working time in the queue
    def show_all(self):
        pass
    
    # TODO(B): Print the current working time
    def show_current(self):
        pass