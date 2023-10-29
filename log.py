class History(object):
    # Record the command history in all session

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
        # Notice: Don't forget to write a session line into stats file!
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