import os

LEAF_LEVEL = 999

class Line(object):
    def __init__(self, text, next):
        self.text = text
        self.next = next
        self.deleted = 0
        # level is only useful for caption, for text, set it as LEAF_LEVEL
        self.level = LEAF_LEVEL

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
        return self.rank + ' ' + self.text

    # TODO(B): Tree show the Unordered list, use point
    def tree_show(self, tab, has_brother):
        if has_brother:
            prefix = "├──"
        else:
            prefix = "└──"
            
        return tab + prefix + self.rank + self.text


class OrderedList(Line):
    # For OrderedList, rank belike 1 2 3 4…
    def __init__(self, text, next, rank):
        super(OrderedList, self).__init__(text, next)
        self.rank = rank

    # TODO(B): to reuse in save, return the output string ######################
    def show(self):
        return str(self.rank) + '. ' + self.text

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
        first_line = True
        f = open(self.file_name, 'w', encoding='gbk')
        cur = self.head
        while cur.next is not None:
            cur = cur.next
            if not cur.deleted:
                if first_line:
                    first_line = False
                    f.write(cur.show())
                else:
                    f.write('\n' + cur.show())
                
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
    def dir_show(self, text):
        line_list = []
        start_pos = 0
        end_pos = self.count
        i = 0
        find_start = False
        find_end = False
        text_level = LEAF_LEVEL + 1
        cur = self.head
        while cur.next is not None:
            cur = cur.next
            if not cur.deleted:
                line_list.append(cur)

                if cur.text == text:
                    start_pos = i
                    text_level = cur.level
                    find_start = True
                
                if find_start and not find_end and cur.level <= text_level:
                    end_pos = i - 1
                    find_end = True
        
                i += 1
        
        self.dir_show_real(start_pos, min(end_pos, len(line_list) - 1), line_list, 0)
    
    def dir_show_real(self, start_pos, end_pos, line_list, tab_num):
        if start_pos > end_pos:
            return
        
        cur_level_pos_list = []
        low_level = LEAF_LEVEL + 1
        for i in range(start_pos, end_pos + 1):
            if line_list[i].level <= low_level:
                low_level = line_list[i].level
                cur_level_pos_list.append(i)
        
        # print cur level and recursively call dir_show_real
        for i in range(len(cur_level_pos_list)):
            has_brother = True if i != len(cur_level_pos_list) - 1 and cur_level_pos_list[i] == cur_level_pos_list[i + 1] - 1 else False
            print(line_list[cur_level_pos_list[i]].tree_show(tab_num * "   ", has_brother))
            if i != len(cur_level_pos_list) - 1:
                self.dir_show_real(cur_level_pos_list[i] + 1, cur_level_pos_list[i + 1] - 1, line_list, tab_num + 1)
            else:
                self.dir_show_real(cur_level_pos_list[i] + 1, end_pos, line_list, tab_num + 1)


    # TODO(B): Call dir_show for each top-level caption
    def tree_show(self):
        line_list = []
        cur = self.head
        while cur.next is not None:
            cur = cur.next
            if not cur.deleted:
                line_list.append(cur)
        
        self.dir_show_real(0, len(line_list) - 1, line_list, 0)
