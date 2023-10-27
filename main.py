

class Line(object):
    pass


def Singleton(cls):
    instance = {}
    def inner(*args, **kargs):
        if (cls not in instance):
            instance[cls] = cls(*args, **kargs)
        return instance[cls]
    return inner


@Singleton
class LineList(object):
    # A linked list to maintain the contents of documents.

    def __init__(self, name):
        self.head = name
    
    def load(self, file):
        self.file_name = file
        pass
    
    def save(self):
        pass

    # TODO: insert the text in pos
    def insert(self, pos, text):
        pass

    # TODO: delete the node in pos
    def delete(self, pos):
        pass


class Adapter(object):
    pass


class Command(object):
    pass


class CommandQueue(object):
    # A queue used to maintain all commands

    def __init__(self):
        self.tail = 0
        self.queue = {}

    # TODO: push a command in the end of queue
    def push(self):
        pass
    
    # TODO: execute the command
    def excute(self):
        pass

    # TODO: redo the last command, can call excute
    def redo(self):
        pass

    # TODO: undo the last command
    def undo(self):
        pass