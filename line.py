
class Line(object):
    def __init__(self, text, deleted, next):
        self.text = text
        self.deleted = deleted
        self.next = next

class Caption(Line):
    # TODO(B): print the caption
    def show():
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

    def __init__(self):
        # Avoid boundary errors by placing an empty node at the head
        self.head = Line("", 0, None)

    # TODO(B): load the file, create a Line object for each line in file
    def load(self, file):
        self.file_name = file
        pass

    # TODO(B): save the file
    def save(self):
        pass

    # TODO(A): find the item before pos, implement it if you think it's helpful
    def find(self, pos):
        pass

    # TODO(A): insert the text before pos
    def insert(self, pos, text):
        pass

    # TODO(A): delete the node in pos
    def delete(self, pos):
        pass
