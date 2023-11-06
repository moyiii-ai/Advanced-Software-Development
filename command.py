from json import load
from line import *

list = LineList()


class Command(object):
    pass


class Load(Command):
    def __init__(self, file):
        self.file = file

    def excute(self):
        list.load(self.file)


class Save(Command):
    def excute(self):
        list.save()


class Insert(Command):
    def __init__(self, number, text):
        self.number = number
        self.text = text

    def excute(self):
        list.insert(self.number, self.text)

    def undo(self):
        list.delete_pos(self.number)


class AppendHead(Command):
    def __init__(self, text):
        self.text = text

    def excute(self):
        list.insert(1, self.text)

    def undo(self):
        list.delete_pos(1)


class AppendTail(Command):
    def __init__(self, text):
        self.text = text

    def excute(self):
        list.insert(list.count + 1, self.text)

    def undo(self):
        list.delete_pos(list.count)


class DeleteText(Command):
    def __init__(self, text):
        self.text = text

    def excute(self):
        list.delete_text(self.text)

    def undo(self):
        list.recover(self.text)


class DeletePos(Command):
    def __init__(self, number):
        self.number = number

    def excute(self):
        self.text = list.delete_pos(self.number)

    def undo(self):
        list.recover(self.text)
        print('undoing')


class Show(Command):
    def excute(self):
        list.show()


class TreeShow(Command):
    def excute(self):
        list.tree_show()


class DirShow(Command):
    def __init__(self, dir):
        self.dir = dir

    def excute(self):
        list.dir_show(self.dir)


class CommandQueue(object):
    # A queue used to maintain all commands

    def __init__(self):
        # As we need to undo and redo, use a list to implement queue
        self.tail = 0
        self.end = 0
        self.queue = []

    def get_command_name(self, command):
        return str(command).split(' ')[0][9:]

    # TODO(A): Execute by calling excute(), push it in the end of queue ########
    def excute(self, command):
        # Notice: for the load/save command, clear the queue as they can't undo
        # For any command, set end equals to tail, as now we can't redo
        command.excute()
        cmd_name = self.get_command_name(command)
        if cmd_name == 'Load' or cmd_name == 'Save':
            self.tail = 0
            self.end = 0
            self.queue = []
            return
        if (cmd_name == 'Show' or cmd_name == 'DirShow' or
                cmd_name == 'TreeShow'):
            return

        self.queue.insert(self.tail, command)
        self.tail = self.tail + 1
        self.end = self.tail

    # TODO(A): Undo the last command ###########################################
    def undo(self):
        # Notice: skip the list/list-tree/dir-tree, but no load/save
        # Move the tail forward, but don't change the end.
        '''while self.tail > 1:
            self.tail -= 1
            cmd_name = self.get_command_name()
            if cmd_name == 'Load' or cmd_name == 'Save':
                break
            if (cmd_name == 'Show' or cmd_name == 'DirShow' or
                    cmd_name == 'TreeShow'):
                continue'''

        if len(self.queue) >= self.tail > 0:
            self.tail -= 1
            self.queue[self.tail].undo()

    # TODO(A): Redo the last command, just call command.excute() again #########
    def redo(self):
        # Notice: we can redo only if tail < end.
        if not self.tail < self.end:
            return
        '''while True:
            self.tail += 1
            cmd_name = self.get_command_name()
            if cmd_name == 'Load' or cmd_name == 'Save':
                break
            if (cmd_name == 'Show' or cmd_name == 'DirShow'
                    or cmd_name == 'TreeShow'):
                continue'''

        self.queue[self.tail].excute()
        self.tail += 1

