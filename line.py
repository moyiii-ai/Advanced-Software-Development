
class Line(object):
    def __init__(self, text, deleted, next):
        self.text = text
        self.deleted = deleted
        self.next = next

class Caption(Line):
    # TODO(B)
    def list(self):
        pass
    
    # TODO(B)
    def tree_list(self, level, has_brother):
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
        self.count = 0

    # TODO(B): Load the file, create a Line object for each line in file
    def load(self, file):
        self.file_name = file
        pass

    # TODO(B): Save the file
    def save(self):
        pass

    # TODO(A): Find the item before pos, implement it if you think it's helpful
    def find(self, pos):
        pass

    # TODO(A): Insert the text before pos
    def insert(self, pos, text):
        pass

    # TODO(A): Delete the node in pos
    def delete(self, pos):
        pass

    # TODO(B)
    def list(self):
        pass

    # TODO(B)
    def tree_list(self):
        pass
