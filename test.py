import unittest
from unittest.mock import patch
from io import StringIO
import os
import shutil
import subprocess

import main

output_template = "Session is over\n"


class TestCLI(unittest.TestCase):
    def setUp(self):
        shutil.rmtree("test_dir", ignore_errors=True)
        # create test directory
        try:
            os.mkdir("test_dir")
        except:
            print("mkdir test_dir failed")
        # switch to test directory
        os.chdir("test_dir")

    def tearDown(self):
        # switch to parent directory
        os.chdir("..")
        # remove test directory
        try:
            shutil.rmtree("test_dir")
        except:
            print("rm test_dir failed")

    def test_quit_command(self):
        command_list = ["quit"]
        with open("inputs.txt", "w") as f:
            f.write("\n".join(command_list))
        with open("inputs.txt", "r") as f:
            with open("outputs.txt", "w") as out:
                subprocess.call(["python", "../main.py"], stdin=f, stdout=out)
        with open("outputs.txt", "r") as f:
            output = f.read()

        expected_output = "" + output_template
        self.assertIn(expected_output, output)

    # load existing file
    def test_load_1(self):
        # create a file
        with open("test.md", "w") as f:
            f.write("test")

        command_list = ["load test.md", "quit"]
        with open("inputs.txt", "w") as f:
            f.write("\n".join(command_list))
        with open("inputs.txt", "r") as f:
            with open("outputs.txt", "w") as out:
                subprocess.call(["python", "../main.py"], stdin=f, stdout=out)

        with open("test.md", "r") as f:
            content = f.read()
        self.assertEqual(content, "test")

    # load non-existing file
    def test_load_one_file_save(self):
        command_list = ["load test.md", "save", "quit"]
        with open("inputs.txt", "w") as f:
            f.write("\n".join(command_list))
        with open("inputs.txt", "r") as f:
            with open("outputs.txt", "w") as out:
                subprocess.call(["python", "../main.py"], stdin=f, stdout=out)

        # check whether the file is created
        files = os.listdir(".")
        self.assertIn("test.md", files)

    # load two non-existing file
    def test_load_two_file_save(self):
        command_list = ["load test.md", "save", "load test_2.md", "save", "quit"]
        with open("inputs.txt", "w") as f:
            f.write("\n".join(command_list))
        with open("inputs.txt", "r") as f:
            with open("outputs.txt", "w") as out:
                subprocess.call(["python", "../main.py"], stdin=f, stdout=out)

        # check whether the file is created
        files = os.listdir(".")
        self.assertIn("test.md", files)
        self.assertIn("test_2.md", files)

    # insert one line
    def test_insert_1(self):
        command_list = ["load test.md", "insert + a", "save", "quit"]
        with open("inputs.txt", "w") as f:
            f.write("\n".join(command_list))
        with open("inputs.txt", "r") as f:
            with open("outputs.txt", "w") as out:
                subprocess.call(["python", "../main.py"], stdin=f, stdout=out)

        with open("test.md", "r") as f:
            content = f.read()
        self.assertEqual(content, "+ a")

    # insert two lines
    def test_insert_2(self):
        command_list = ["load test.md", "insert + a", "insert + b", "save", "quit"]
        with open("inputs.txt", "w") as f:
            f.write("\n".join(command_list))
        with open("inputs.txt", "r") as f:
            with open("outputs.txt", "w") as out:
                subprocess.call(["python", "../main.py"], stdin=f, stdout=out)

        with open("test.md", "r") as f:
            content = f.read()
        self.assertEqual(content, "+ a\n+ b")

    # insert two lines with position
    def test_insert_3(self):
        command_list = ["load test.md", "insert + a", "insert 1 + b", "save", "quit"]
        with open("inputs.txt", "w") as f:
            f.write("\n".join(command_list))
        with open("inputs.txt", "r") as f:
            with open("outputs.txt", "w") as out:
                subprocess.call(["python", "../main.py"], stdin=f, stdout=out)

        with open("test.md", "r") as f:
            content = f.read()
        self.assertEqual(content, "+ b\n+ a")

    # insert three lines with position
    def test_insert_4(self):
        command_list = [
            "load test.md",
            "insert + a",
            "insert 1 + b",
            "insert 1 + c",
            "save",
            "quit",
        ]
        with open("inputs.txt", "w") as f:
            f.write("\n".join(command_list))
        with open("inputs.txt", "r") as f:
            with open("outputs.txt", "w") as out:
                subprocess.call(["python", "../main.py"], stdin=f, stdout=out)

        with open("test.md", "r") as f:
            content = f.read()
        self.assertEqual(content, "+ c\n+ b\n+ a")

    # overflow line insert
    def test_insert_5(self):
        command_list = ["load test.md", "insert + a", "insert 3 + b", "save", "quit"]
        with open("inputs.txt", "w") as f:
            f.write("\n".join(command_list))
        with open("inputs.txt", "r") as f:
            with open("outputs.txt", "w") as out:
                subprocess.call(["python", "../main.py"], stdin=f, stdout=out)

        with open("test.md", "r") as f:
            content = f.read()
        self.assertEqual(content, "+ a\n+ b")

    # insert line to existing file
    def test_insert_6(self):
        command_list = [
            "load test.md",
            "insert + a",
            "save",
            "load test.md",
            "insert 1 + b",
            "save",
            "quit",
        ]
        with open("inputs.txt", "w") as f:
            f.write("\n".join(command_list))
        with open("inputs.txt", "r") as f:
            with open("outputs.txt", "w") as out:
                subprocess.call(["python", "../main.py"], stdin=f, stdout=out)

        with open("test.md", "r") as f:
            content = f.read()
        self.assertEqual(content, "+ b\n+ a")
    
    # modify two files
    def test_multi_file_1(self):
        command_list = [
            "load test.md",
            "insert + a",
            "save",
            "load test_2.md",
            "insert + b",
            "save",
            "load test.md",
            "insert 1 + c",
            "save",
            "load test_2.md",
            "insert 1 + d",
            "save",
            "load test.md",
            "list",
            "load test_2.md",
            "list",
            "insert - e",
            "list",
            "save",
            "quit"
        ]
        with open("inputs.txt","w") as f:
            f.write("\n".join(command_list))
        with open("inputs.txt","r") as f:
            with open("outputs.txt","w") as out:
                subprocess.call(["python","../main.py"],stdin=f,stdout=out)
        
        with open("test.md","r") as f:
            content = f.read()
        self.assertEqual(content, "+ c\n+ a")
        with open("test_2.md","r") as f:
            content = f.read()
        self.assertEqual(content, "+ d\n+ b\n- e")

        with open("outputs.txt","r") as f:
            content = f.read()
            self.assertIn("+ c\n+ a", content)
            self.assertIn("+ d\n+ b", content)
            pos_1 = content.find("+ d\n+ b")
            pos_2 = content.find("+ d\n+ b", pos_1 + 1)
            self.assertNotEqual(pos_2, -1)
            self.assertIn("+ d\n+ b\n- e", content)

    # append head once
    def test_append_head_1(self):
        command_list = ["load test.md", "append-head + a", "save", "quit"]
        with open("inputs.txt", "w") as f:
            f.write("\n".join(command_list))
        with open("inputs.txt", "r") as f:
            with open("outputs.txt", "w") as out:
                subprocess.call(["python", "../main.py"], stdin=f, stdout=out)

        with open("test.md", "r") as f:
            content = f.read()
        self.assertEqual(content, "+ a")

    # append head twice
    def test_append_head_2(self):
        command_list = [
            "load test.md",
            "append-head + a",
            "append-head + b",
            "save",
            "quit",
        ]
        with open("inputs.txt", "w") as f:
            f.write("\n".join(command_list))
        with open("inputs.txt", "r") as f:
            with open("outputs.txt", "w") as out:
                subprocess.call(["python", "../main.py"], stdin=f, stdout=out)

        with open("test.md", "r") as f:
            content = f.read()
        self.assertEqual(content, "+ b\n+ a")

    # append head once
    def test_append_head_3(self):
        command_list = [
            "load test.md",
            "insert + a",
            "append-head + b",
            "save",
            "quit",
        ]
        with open("inputs.txt", "w") as f:
            f.write("\n".join(command_list))
        with open("inputs.txt", "r") as f:
            with open("outputs.txt", "w") as out:
                subprocess.call(["python", "../main.py"], stdin=f, stdout=out)

        with open("test.md", "r") as f:
            content = f.read()
        self.assertEqual(content, "+ b\n+ a")

    # append tail once
    def test_append_tail_1(self):
        command_list = ["load test.md", "append-tail + a", "save", "quit"]
        with open("inputs.txt", "w") as f:
            f.write("\n".join(command_list))
        with open("inputs.txt", "r") as f:
            with open("outputs.txt", "w") as out:
                subprocess.call(["python", "../main.py"], stdin=f, stdout=out)

        with open("test.md", "r") as f:
            content = f.read()
        self.assertEqual(content, "+ a")

    # append tail twice
    def test_append_tail_2(self):
        command_list = [
            "load test.md",
            "append-tail + a",
            "append-tail + b",
            "save",
            "quit",
        ]
        with open("inputs.txt", "w") as f:
            f.write("\n".join(command_list))
        with open("inputs.txt", "r") as f:
            with open("outputs.txt", "w") as out:
                subprocess.call(["python", "../main.py"], stdin=f, stdout=out)

        with open("test.md", "r") as f:
            content = f.read()
        self.assertEqual(content, "+ a\n+ b")

    # mix append head and append tail
    def test_mix_head_tail(self):
        command_list = [
            "load test.md",
            "append-tail + a",
            "append-head + b",
            "append-tail + c",
            "append-head + d",
            "save",
            "quit",
        ]
        with open("inputs.txt", "w") as f:
            f.write("\n".join(command_list))
        with open("inputs.txt", "r") as f:
            with open("outputs.txt", "w") as out:
                subprocess.call(["python", "../main.py"], stdin=f, stdout=out)

        with open("test.md", "r") as f:
            content = f.read()
        self.assertEqual(content, "+ d\n+ b\n+ a\n+ c")

    # delete with line number
    def test_delete_number_1(self):
        command_list = ["load test.md", "insert + a", "delete 1", "save", "quit"]
        with open("inputs.txt", "w") as f:
            f.write("\n".join(command_list))
        with open("inputs.txt", "r") as f:
            with open("outputs.txt", "w") as out:
                subprocess.call(["python", "../main.py"], stdin=f, stdout=out)

        with open("test.md", "r") as f:
            content = f.read()
        self.assertEqual(content, "")

    # mix insert and delete with line number
    def test_mix_insert_delete_number_1(self):
        command_list = [
            "load test.md",
            "insert + a",
            "insert + b",
            "insert + c",
            "delete 2",
            "insert 2 + d",
            "insert 1 + e",
            "delete 1",
            "insert 2 + f",
            "delete 4",
            "save",
            "quit",
        ]
        with open("inputs.txt", "w") as f:
            f.write("\n".join(command_list))
        with open("inputs.txt", "r") as f:
            with open("outputs.txt", "w") as out:
                subprocess.call(["python", "../main.py"], stdin=f, stdout=out)

        with open("test.md", "r") as f:
            content = f.read()
        self.assertEqual(content, "+ a\n+ f\n+ d")

    # delete with line content
    def test_delete_content_1(self):
        command_list = ["load test.md", "insert # a", "delete a", "save", "quit"]
        with open("inputs.txt", "w") as f:
            f.write("\n".join(command_list))
        with open("inputs.txt", "r") as f:
            with open("outputs.txt", "w") as out:
                subprocess.call(["python", "../main.py"], stdin=f, stdout=out)

        with open("test.md", "r") as f:
            content = f.read()
        self.assertEqual(content, "")

    # mix insert and delete with line content
    def test_mix_insert_delete_content_1(self):
        command_list = [
            "load test.md",
            "insert # a",
            "insert ## b",
            "insert ### c",
            "delete b",
            "insert # d",
            "insert # e",
            "delete e",
            "insert # f",
            "delete f",
            "save",
            "quit",
        ]
        with open("inputs.txt", "w") as f:
            f.write("\n".join(command_list))
        with open("inputs.txt", "r") as f:
            with open("outputs.txt", "w") as out:
                subprocess.call(["python", "../main.py"], stdin=f, stdout=out)

        with open("test.md", "r") as f:
            content = f.read()
        self.assertEqual(content, "# a\n### c\n# d")

    # test undo
    def test_undo_1(self):
        command_list = [
            "load test.md",
            "insert + a",
            "undo",
            "append-head + b",
            "undo",
            "append-tail + c",
            "undo",
            "insert + a",
            "delete a",
            "undo",
            "insert + b",
            "delete 2",
            "undo",
            "save",
            "quit",
        ]
        with open("inputs.txt", "w") as f: 
            f.write("\n".join(command_list))
        with open("inputs.txt", "r") as f:
            with open("outputs.txt", "w") as out:
                subprocess.call(["python", "../main.py"], stdin=f, stdout=out)

        with open("test.md", "r") as f:
            content = f.read()
        self.assertEqual(content, "+ a\n+ b")

    # test undo
    def test_undo_2(self):
        command_list = [
            "load test.md",
            "insert - a",
            "append-head - b",
            "undo",
            "insert - c",
            "delete c",
            "undo",
            "save",
            "quit",
        ]
        with open("inputs.txt", "w") as f: 
            f.write("\n".join(command_list))
        with open("inputs.txt", "r") as f:
            with open("outputs.txt", "w") as out:
                subprocess.call(["python", "../main.py"], stdin=f, stdout=out)

        with open("test.md", "r") as f:
            content = f.read()
        self.assertEqual(content, "- a\n- c")
    
    # test undo
    def test_undo_3(self):
        command_list = [
            "load test.md",
            "insert * a",
            "delete a",
            "undo",
            "insert * c",
            "delete c",
            "undo",
            "undo",
            "undo",
            "save",
            "quit",
        ]
        with open("inputs.txt", "w") as f: 
            f.write("\n".join(command_list))
        with open("inputs.txt", "r") as f:
            with open("outputs.txt", "w") as out: 
                subprocess.call(["python","../main.py"],stdin=f,stdout=out)

        with open("test.md","r") as f:
            content = f.read()
        self.assertEqual(content, "")
    
    # test redo
    def test_redo_1(self):
        commend_list = [
            "load test.md",
            "insert + a",
            "undo",
            "redo",
            "insert + b",
            "delete b",
            "undo",
            "undo",
            "redo",
            "redo",
            "save",
            "quit",
        ]
        with open("inputs.txt", "w") as f:
            f.write("\n".join(commend_list))
        with open("inputs.txt", "r") as f:
            with open("outputs.txt", "w") as out:
                subprocess.call(["python","../main.py"], stdin=f, stdout=out)
        
        with open("test.md", "r") as f:
            content = f.read()
        self.assertEqual(content, "+ a")
    
    # test list
    def test_list_1(self):
        command_list = [
            "load test.md",
            "insert + a",
            "insert - b",
            "insert * c",
            "insert 1. d",
            "insert 2. e",
            "insert # f",
            "insert ## g",
            "insert ### h",
            "list",
            "quit"
        ]
        with open("inputs.txt", "w") as f:
            f.write("\n".join(command_list))
        with open("inputs.txt","r") as f:
            with open("outputs.txt","w") as out:
                subprocess.call(["python","../main.py"],stdin=f,stdout=out)
        
        with open("outputs.txt","r") as f:
            content = f.read()
        expected_content = "+ a\n- b\n* c\n1. d\n2. e\n# f\n## g\n### h\n"
        self.assertIn(expected_content, content)
    
    # test list tree
    def test_list_tree_1(self):
        command_list = [
            "load test.md",
            "insert # a",
            "insert ## b",
            "insert # c",
            "insert # d",
            "insert + e",
            "insert # f",
            "insert ## g",
            "insert 1. h",
            "insert 2. i",
            "insert # j",
            "insert ## k",
            "insert ## l",
            "insert ### m",
            "insert - n",
            "insert * o",
            "list-tree",
            "quit"
        ]
        with open("inputs.txt", "w") as f:
            f.write("\n".join(command_list))
        with open("inputs.txt","r") as f:
            with open("outputs.txt","w") as out:
                subprocess.call(["python","../main.py"],stdin=f,stdout=out)

        with open("outputs.txt","r") as f:
            content = f.read()
        expected_content = "└──a\n   └──b\n├──c\n└──d\n   └──+e\n└──f\n   └──g\n      ├──1.h\n      └──2.i\n└──j\n   ├──k\n   └──l\n      └──m\n         ├──-n\n         └──*o\n"
        self.assertIn(expected_content, content)
    
    # test dir tree
    def test_dir_tree_1(self):
        command_list = [
            "load test.md",
            "insert - a",
            "insert ### b",
            "insert ## c",
            "insert # d",
            "insert + e",
            "insert # f",
            "insert ## g",
            "insert 1. h",
            "insert 2. i",
            "insert # j",
            "insert ## k",
            "insert ## l",
            "insert ### m",
            "insert - n",
            "insert * o",
            "dir-tree",
            "quit"
        ]
        with open("inputs.txt", "w") as f:
            f.write("\n".join(command_list))
        with open("inputs.txt","r") as f:
            with open("outputs.txt","w") as out:
                subprocess.call(["python","../main.py"],stdin=f,stdout=out)

        with open("outputs.txt","r") as f:
            content = f.read()
        expected_content = "├──-a\n├──b\n├──c\n└──d\n   └──+e\n└──f\n   └──g\n      ├──1.h\n      └──2.i\n└──j\n   ├──k\n   └──l\n      └──m\n         ├──-n\n         └──*o\n"
        self.assertIn(expected_content, content)

    # test dir tree
    def test_dir_tree_2(self):
        command_list = [
            "load test.md",
            "insert - a",
            "insert ### b",
            "insert ## c",
            "insert # d",
            "insert + e",
            "insert # f",
            "insert ## g",
            "insert 1. h",
            "insert 2. i",
            "insert # j",
            "insert ## k",
            "insert ## l",
            "insert ### m",
            "insert - n",
            "insert * o",
            "dir-tree a",
            "quit"
        ]
        with open("inputs.txt", "w") as f:
            f.write("\n".join(command_list))
        with open("inputs.txt","r") as f:
            with open("outputs.txt","w") as out:
                subprocess.call(["python","../main.py"],stdin=f,stdout=out)

        with open("outputs.txt","r") as f:
            content = f.read()
        expected_content = "└──-a"
        self.assertIn(expected_content, content)

    # test dir tree
    def test_dir_tree_3(self):
        command_list = [
            "load test.md",
            "insert - a",
            "insert ### b",
            "insert ## c",
            "insert # d",
            "insert + e",
            "insert # f",
            "insert ## g",
            "insert 1. h",
            "insert 2. i",
            "insert # j",
            "insert ## k",
            "insert ## l",
            "insert ### m",
            "insert - n",
            "insert * o",
            "dir-tree d",
            "quit"
        ]
        with open("inputs.txt", "w") as f:
            f.write("\n".join(command_list))
        with open("inputs.txt","r") as f:
            with open("outputs.txt","w") as out:
                subprocess.call(["python","../main.py"],stdin=f,stdout=out)

        with open("outputs.txt","r") as f:
            content = f.read()
        expected_content = "└──d\n   └──+e"
        self.assertIn(expected_content, content)
    
    # test dir tree
    def test_dir_tree_4(self):
        command_list = [
            "load test.md",
            "insert - a",
            "insert ### b",
            "insert ## c",
            "insert # d",
            "insert + e",
            "insert # f",
            "insert ## g",
            "insert 1. h",
            "insert 2. i",
            "insert # j",
            "insert ## k",
            "insert ## l",
            "insert ### m",
            "insert - n",
            "insert * o",
            "dir-tree j",
            "quit"
        ]
        with open("inputs.txt", "w") as f:
            f.write("\n".join(command_list))
        with open("inputs.txt","r") as f:
            with open("outputs.txt","w") as out:
                subprocess.call(["python","../main.py"],stdin=f,stdout=out)

        with open("outputs.txt","r") as f:
            content = f.read()
        expected_content = "└──j\n   ├──k\n   └──l\n      └──m\n         ├──-n\n         └──*o"
        self.assertIn(expected_content, content)

    # test dir tree
    def test_dir_tree_5(self):
        command_list = [
            "load test.md",
            "insert - a",
            "insert ### b",
            "insert ## c",
            "insert # d",
            "insert + e",
            "insert # f",
            "insert ## g",
            "insert 1. h",
            "insert 2. i",
            "insert # j",
            "insert ## k",
            "insert ## l",
            "insert ### m",
            "insert - n",
            "insert * o",
            "dir-tree l",
            "quit"
        ]
        with open("inputs.txt", "w") as f:
            f.write("\n".join(command_list))
        with open("inputs.txt","r") as f:
            with open("outputs.txt","w") as out:
                subprocess.call(["python","../main.py"],stdin=f,stdout=out)

        with open("outputs.txt","r") as f:
            content = f.read()
        expected_content = "└──l\n   └──m\n      ├──-n\n      └──*o\n"
        self.assertIn(expected_content, content)
    
    # test dir tree
    def test_dir_tree_6(self):
        command_list = [
            "load test.md",
            "insert - a",
            "insert ### b",
            "insert ## c",
            "insert # d",
            "insert + e",
            "insert # f",
            "insert ## g",
            "insert 1. h",
            "insert 2. i",
            "insert # j",
            "insert ## k",
            "insert ## l",
            "insert ### m",
            "insert - n",
            "insert * o",
            "dir-tree k",
            "quit"
        ]
        with open("inputs.txt", "w") as f:
            f.write("\n".join(command_list))
        with open("inputs.txt","r") as f:
            with open("outputs.txt","w") as out:
                subprocess.call(["python","../main.py"],stdin=f,stdout=out)

        with open("outputs.txt","r") as f:
            content = f.read()
        expected_content = "└──k"
        self.assertIn(expected_content, content)

if __name__ == "__main__":
    unittest.main()
