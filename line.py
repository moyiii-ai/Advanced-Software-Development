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

    # TODO(B): load the file
    def load(self, file):
        self.file_name = file
        pass

    # TODO(B): save the file
    def save(self):
        pass

    # TODO(A): find the Line before pos, implement it if you think it's helpful
    def find(self, pos):
        pass

    # TODO(A): insert the text in pos
    def insert(self, pos, text):
        pass

    # TODO(A): delete the node in pos
    def delete(self, pos):
        pass
