import os


class Line(object):
    def __init__(self, text, next):
        self.text = text
        self.next = next
        self.deleted = 0
        # level is only useful for caption, for text, set it as 0
        self.level = 0

    # TODO(B): to reuse in save, return the output string ######################
    def show(self):
        return self.text


class Caption(Line):
    def __init__(self, text, next, level):
        super(Caption, self).__init__(text, next)
        self.level = level

    # TODO(B): to reuse in save, return the output string ######################
    def show(self):
        return self.level * '#' + ' ' + self.text

    # TODO(B)
    def tree_show(self, tab, has_brother):
        if has_brother:
            prefix = "├──"
        else:
            prefix = "└──"
            
        return tab + prefix + self.text
        
        #pass


class UnorderedList(Line):
    def __init__(self, text, next, rank):
        super(UnorderedList, self).__init__(text, next)
        self.rank = rank

    # TODO(B): to reuse in save, return the output string ######################
    def show(self):
        if self.rank == 1:
            tag = "-"
        elif self.rank == 2:
            tag = "+"
        elif self.rank == 3:
            tag = "*"
        return tag + ' ' + self.text

    # TODO(B): Tree show the Unordered list, use point
    def tree_show(self, tab, has_brother):
        if has_brother:
            prefix = "├──"
        else:
            prefix = "└──"
            
        if self.rank == 1:
            tag = "-"
        elif self.rank == 2:
            tag = "+"
        elif self.rank == 3:
            tag = "*"
        return tab + prefix + tag + self.text
        
        #pass


class OrderedList(Line):
    # For OrderedList, rank belike 1 2 3 4…
    def __init__(self, text, next, rank):
        super(OrderedList, self).__init__(text, next)
        self.rank = rank

    # TODO(B): to reuse in save, return the output string ######################
    def show(self):
        return str(self.rank) + '.' + self.text

    # TODO(B): rank is only useful for OrderedList
    def tree_show(self, tab, has_brother):
        if has_brother:
            prefix = "├──"
        else:
            prefix = "└──"
        return tab + prefix + str(self.rank) + '.' + self.text
        #pass


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
        self.head = Line("", None)
        self.count = 0

    def line_creation(self, cur, line):
        line = line.strip('\n')
        # Remove all the \n which is unnecessary
        # Here, we have to decide what type the line is and create instance
        if line[0] == '*' or line[0] == '+' or line[0] == '-':
            # Unordered list, start with * + -, record the tag and text #
            cur.next = UnorderedList(line[2:], None, line[0])
            cur = cur.next
            self.count += 1
        elif line[0].isdigit():
            # Ordered list, start with a number and a point, record rank
            for i in range(len(line)):
                if not line[i].isdigit():
                    if line[i] == '.':
                        cur.next = OrderedList(line[i + 2:], None,
                                               int(line[0:i]))
                        cur = cur.next
                        self.count += 1
                    else:
                        break
        elif line[0] == '#':
            # Caption, start with many #, the number of # is same as its level #
            for i in range(len(line)):
                if line[i] != '#':
                    cur.next = Caption(line[i + 1:], None, i)
                    cur = cur.next
                    self.count += 1
                    break
        else:
            # Default line #
            cur.next = Line(line, None)
            cur = cur.next
            self.count += 1

        return cur

    # TODO(B): Load the file, create a Line object for each line in file #######
    def load(self, file):
        self.file_name = file
        # when saving, the filename is not given, so record the name here #
        if os.path.exists(self.file_name):
            openfile = open(self.file_name, 'r', encoding='gbk')
            print('Load file:', file)
        else:
            file = open(self.file_name, 'w')
            file.close()
            print('Create file:', file)
            openfile = open(self.file_name, 'r', encoding='gbk')
            print('Load file:', file)

        lines = openfile.readlines()
        cur = self.head
        for line in lines:
            cur = self.line_creation(cur, line)

        # self.show()
        # print(self.count)
        openfile.close()

    # TODO(B): Save the file ###################################################
    def save(self):
        # Notice: Only save the lines without deleted tag!
        f = open(self.file_name, 'w', encoding='gbk')
        cur = self.head
        while cur.next is not None:
            cur = cur.next
            if not cur.deleted:
                f.write(cur.show())
        f.close()

    # TODO(A): Insert the text at pos ##########################################
    def insert(self, pos, text):
        # Notice: Don't forget to update self.count!
        # judge the type of text and create different kinds of line
        cur = self.head
        while pos > 1 and cur.next is not None:
            cur = cur.next
            if cur.deleted:
                continue
            pos -= 1

        foll = cur.next
        cur = self.line_creation(cur, text)
        cur.next = foll

    # TODO(A): Delete the node by text, just mark the deleted tag ##############
    def delete_text(self, text):
        # Notice: Don't forget to update self.count!
        cur = self.head
        while cur.next is not None:
            cur = cur.next
            if not cur.deleted:
                if cur.text == text:
                    cur.deleted = 1
                    self.count -= 1
                    break

    # TODO(A): Delete the node in pos and return the text ######################
    def delete_pos(self, pos):
        cur = self.head
        if pos > self.count:
            print('Deleting Out of Range!')
            return
        while pos > 0:
            cur = cur.next
            if cur.deleted:
                continue
            pos -= 1

        text = cur.text
        cur.deleted = 1
        self.count -= 1
        return text

    # TODO(A): Remove the delete tag by text ###################################
    def recover(self, text):
        cur = self.head
        while cur.next is not None:
            cur = cur.next
            if cur.deleted:
                if cur.text == text:
                    cur.deleted = 0
                    self.count += 1
                    break

    # TODO(B): Just call show for each line ####################################
    def show(self):
        # traverse the list, print everything without delete tag #
        cur = self.head
        while cur.next is not None:
            cur = cur.next
            if not cur.deleted:
                print(cur.show())

    # TODO(B): Recursively call dir_show for each subtree
    def dir_show(self, text, start_level, level, has_brother):

        cur = self.head
        
        while cur.next is not None:
            cur = cur.next
            if not cur.deleted:
                if cur.text == text:
                    if level == 0 and not has_brother:
                        start_level = cur.level
                    level = cur.level
                    break

        tab_num = level - start_level
        if type(cur) == Line:
            print(cur.show())
        else:
            print(cur.tree_show(tab_num * "   ", has_brother))

        if not level:
            return

        children = []
        children_level = []
        upper_bound = level + 1000
        
        while True:
            if cur is None:
                break
            cur = cur.next
            if cur is None:
                break
            if not cur.deleted:
                #print(cur.level, upper_bound, level)
                if cur.level <= level and cur.level != 0:
                    break
                if cur.level > upper_bound:
                    continue
                elif cur.level > level or cur.level == 0:
                    upper_bound = cur.level
                    children.append(cur)
                    if cur.level:
                        children_level.append(cur.level)
                    else:
                        children_level.append(upper_bound + 1)

                    
        for i in range(len(children)):
            self.dir_show(children[i].text, start_level, children_level[i], False if i == len(children) - 1 else True)


    # TODO(B): Call dir_show for each top-level caption
    def tree_show(self):
        cur = self.head
        if cur.next is not None:
            cur = cur.next
            top_level = cur.level
            top_captions = [cur]
        
        while cur.next is not None:
            cur = cur.next
            if not cur.deleted:
                if cur.level == top_level:
                    top_captions.append(cur)
        
        for i in range(len(top_captions)):
            self.dir_show(top_captions[i].text, top_captions[i].level, top_captions[i].level, False if i == len(top_captions) - 1 else True)
        #pass
