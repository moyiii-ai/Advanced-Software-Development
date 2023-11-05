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


if __name__ == "__main__":
    unittest.main()
