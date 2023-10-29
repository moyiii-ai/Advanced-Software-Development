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
        list.dir_show(self.dir, 0, 0)


class CommandQueue(object):
    # A queue used to maintain all commands

    def __init__(self):
        # As we need to undo and redo, use a list to implement queue
        self.tail = 0
        self.queue = {}

    # TODO(A): Execute by calling command.excute(), push it in the end of queue
    def excute(self, command):
        # Notice: for the load/save command, clear the queue as they can't undo
        pass

    # TODO(A): Undo the last command
    def undo(self):
        # Notice: skip the list/list-tree/dir-tree, but no load/save
        pass

    # TODO(A): Redo the last command, just call command.excute()
    def redo(self):
        # Notice: check if the last command is undo
        pass
