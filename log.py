import time

class History(object):
    # Record the command history in all session

    def __init__(self):
        self.tail = 0
        self.queue = {}

    path = "history.log"
    log_file = open(path, "a")
    # Start a new session and load the history file
    def start_session(self):
        # Don't forget to write a session line into history file!
        session_time = time.strftime("%Y%m%d %H:%M:%S")
        self.log_file.write(f"session start at {session_time}\n")
        with open(self.path, "r") as file:
            lines = file.readlines()
            index = 0
            for _, line in enumerate(lines):
                if line.startswith("session start"):
                    continue
                command_time, command = line.strip().split(" ", 1)
                self.queue[index] = (command_time, command)
                index = index + 1
            self.tail = index
    
    # Insert the command to the history buffer, and save it to file
    def push(self, command):
        command_time = time.strftime("%Y%m%d %H:%M:%S")
        self.queue[self.tail] = (command_time, command)
        self.tail += 1
        self.log_file.write(f"{command_time} {command}\n")
    
    # Print the last num history command
    def show_num(self, num):
        if num > self.tail:
            num = self.tail

        for i in range(self.tail - num, self.tail):
            timestamp, command = self.queue[i]
            print(f"{timestamp} {command}")
    
    # Print all history command
    def show_all(self):
        self.show_num(self.tail)


class Statistic(object):
    # Record the working time of all files in the current session

    def __init__(self):
        self.tail = 0
        self.work_time = 0
        self.queue = {}
        self.cur_file = ""

    path = "stats.log"
    stat_file = open(path, "a")
    # Start a new session, clear the queue and load the stats file    
    def start_session(self):
        # Notice: Don't forget to write a session line into stats file!
        self.tail = 0
        self.work_time = 0
        self.queue = {}
        self.cur_file = ""
        session_time = time.strftime("%Y%m%d:%H%M%S")
        self.stat_file.write(f"session start {session_time}\n")

    def quit_session(self):
        for file_name, elapsed_time in self.queue.items():
            days, remainder = divmod(int(elapsed_time), 86400)
            hours, remainder = divmod(remainder, 3600)
            minutes, seconds = divmod(remainder, 60)
            if days > 0:
                self.stat_file.write(f"./{file_name} {days} 天 \
                                     {hours} 小时 {minutes} 分钟\n")
            elif hours > 0:
                self.stat_file.write(f"./{file_name} {hours} 小时 \
                                     {minutes} 分钟\n")
            elif minutes > 0:
                self.stat_file.write(f"./{file_name} {minutes} 分钟\n")
            else:
                self.stat_file.write(f"./{file_name} {seconds} 秒\n")
        
    # Open a new file and record the start time
    # save the working time of last file in the queue and stats file
    def open_file(self, file_name):
        if self.queue:
            last_file = list(self.queue.keys())[-1]
            elapsed_time = time.time() - self.work_time
            self.queue[last_file] += elapsed_time
        if file_name not in list(self.queue.keys()):
            self.queue[file_name] = 0
        else:
            self.queue[file_name] += 0
        self.work_time = time.time()
        self.cur_file = file_name
    
    # Print all working time in the queue
    def show_all(self):
        for file_name, elapsed_time in self.queue.items():
            if file_name == self.cur_file:
                elapsed_time += time.time() - self.work_time
            days, remainder = divmod(int(elapsed_time), 86400)
            hours, remainder = divmod(remainder, 3600)
            minutes, seconds = divmod(remainder, 60)
            if days > 0:
                print(f"./{file_name} {days} 天 {hours} 小时 {minutes} 分钟")
            elif hours > 0:
                print(f"./{file_name} {hours} 小时 {minutes} 分钟")
            elif minutes > 0:
                print(f"./{file_name} {minutes} 分钟")
            else:
                print(f"./{file_name} {seconds} 秒")   
    
    # Print the current working time
    def show_current(self):
        if self.queue:
            elapsed_time = self.queue[self.cur_file]
            elapsed_time += time.time() - self.work_time
            days, remainder = divmod(int(elapsed_time), 86400)
            hours, remainder = divmod(remainder, 3600)
            minutes, seconds = divmod(remainder, 60)
            if days > 0:
                print(f"./{self.cur_file} {days} 天 {hours} 小时 {minutes} 分钟")
            elif hours > 0:
                print(f"./{self.cur_file} {hours} 小时 {minutes} 分钟")
            elif minutes > 0:
                print(f"./{self.cur_file} {minutes} 分钟")
            else:
                print(f"./{self.cur_file} {seconds} 秒")