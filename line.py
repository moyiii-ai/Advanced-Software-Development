class Line(object):
    def __init__(self, text, deleted, next, level):
        self.text = text
        self.deleted = deleted
        self.next = next
        # level is only useful for caption, for text, set it as 0
        self.level = level


class Caption(Line):
    # TODO(B): to reuse in save, return the output string
    def show(self):
        pass
    
    # TODO(B)
    def tree_show(self, tab, has_brother, rank):
        pass


class UnorderedList(Line):
    # TODO(B)
    def show(self):
        pass

    # TODO(B)
    def tree_show(self, tab, has_brother, rank):
        pass


class OrderedList(Line):
    # TODO(B)
    def show(self):
        pass

    # TODO(B): rank is only useful for OrderedList
    def tree_show(self, tab, has_brother, rank):
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
        self.head = Line("", 0, None, 0)
        self.count = 0

    # TODO(B): Load the file, create a Line object for each line in file
    def load(self, file):
        self.file_name = file
        pass

    # TODO(B): Save the file
    def save(self):
        # Notice: Only save the lines without deleted tag!
        pass

    # TODO(A): Insert the text at pos
    def insert(self, pos, text):
        # Notice: Don't forget to update self.count!
        # judge the type of text and create different kinds of line
        pass

    # TODO(A): Delete the node by text, just mark the deleted tag
    def delete_text(self, text):
        # Notice: Don't forget to update self.count!
        pass

    # TODO(A): Delete the node in pos and return the text
    def delete_pos(self, pos):
        # Notice: Don't forget to update self.count!
        pass

    # TODO(A): Remove the delete tag by text
    def recover(self, text):
        pass

    # TODO(B)
    def show(self):
        pass

    # TODO(B)
    def dir_show(self, text, level, has_brother):
        pass

    # TODO(B): call dir_show for each root
    def tree_show(self):
        pass

    
