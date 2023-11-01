import unittest
from unittest.mock import patch
from io import StringIO
import os

import main

output_template = 'Session is over\n'

class TestCLI(unittest.TestCase):
    def setUp(self):
        # create test directory
        try:
            os.mkdir('test_dir')
        except:
            pass
        # switch to test directory
        os.chdir('test_dir')
    
    def tearDown(self):
        # switch to parent directory
        os.chdir('..')
        # remove test directory
        try:
            os.rmdir('test_dir')
        except:
            pass
    
    @patch('builtins.input', side_effect=['quit'])
    def test_quit_command(self, input):
        with patch('sys.stdout', new=StringIO()) as output:
            main.run()
        expected_output = '' + output_template
        self.assertIn(expected_output, output.getvalue())
    
    # load existing file
    @patch('builtins.input', side_effect=['load test.md', 'quit'])
    def test_load_1(self, input):
        # create a file
        with open('test.md', 'w') as f:
            f.write('test')
        
        with patch('sys.stdout', new=StringIO()) as output:
            main.run()

        with open('test.md', 'r') as f:
            content = f.read()
        try:
            os.remove('test.md')
        except:
            pass
        self.assertEqual(content, 'test')
    
    # load non-existing file
    @patch('builtins.input', side_effect=['load test.md', 'save', 'quit'])
    def test_load_one_file_save(self, input):
        with patch('sys.stdout', new=StringIO()) as output:
            main.run()

        # check whether the file is created
        files = os.listdir('.')
        # delete the file
        try:
            os.remove('test.md')
        except:
            pass
        self.assertIn('test.md', files)
    
    # load two non-existing file
    @patch('builtins.input', side_effect=['load test.md', 'save', 'load test_2.md', 'save', 'quit'])
    def test_load_two_file_save(self, input):
        with patch('sys.stdout', new=StringIO()) as output:
            main.run()

        # check whether the file is created
        files = os.listdir('.')
        # delete the file
        try:
            os.remove('test.md')
            os.remove('test_2.md')
        except:
            pass
        self.assertIn('test.md', files)
        self.assertIn('test_2.md', files)
    
    # @patch('builtins.input', side_effect=['load ./test.md', 'save', 'quit'])
    # def test_load_current_dir_file(self, input):
    #     with patch('sys.stdout', new=StringIO()) as output:
    #         main.run()

    #     # check whether the file is created
    #     files = os.listdir('.')
    #     # delete the file
    #     try:
    #         os.remove('test.md')
    #     except:
    #         pass
    #     self.assertIn('test.md', files)
    
    # insert one line
    @patch('builtins.input', side_effect=['load test.md', 'insert a', 'save', 'quit'])
    def test_insert_1(self, input):
        with patch('sys.stdout', new=StringIO()) as output:
            main.run()

        with open('test.md', 'r') as f:
            content = f.read()
        try:
            os.remove('test.md')
        except:
            pass
        self.assertEqual(content, 'a')
    
    # insert two lines
    @patch('builtins.input', side_effect=['load test.md', 'insert a', 'insert b', 'save', 'quit'])
    def test_insert_2(self, input):
        with patch('sys.stdout', new=StringIO()) as output:
            main.run()

        with open('test.md', 'r') as f:
            content = f.read()
        try:
            os.remove('test.md')
        except:
            pass
        self.assertEqual(content, 'a\nb')
    
    # insert two lines with position
    @patch('builtins.input', side_effect=['load test.md', 'insert a', 'insert 1 b', 'save', 'quit'])
    def test_insert_3(self, input):
        with patch('sys.stdout', new=StringIO()) as output:
            main.run()

        with open('test.md', 'r') as f:
            content = f.read()
        try:
            os.remove('test.md')
        except:
            pass
        self.assertEqual(content, 'b\na')
    
    # insert three lines with position
    @patch('builtins.input', side_effect=['load test.md', 'insert a', 'insert 1 b', 'insert 1 c', 'save', 'quit'])
    def test_insert_4(self, input):
        with patch('sys.stdout', new=StringIO()) as output:
            main.run()

        with open('test.md', 'r') as f:
            content = f.read()
        try:
            os.remove('test.md')
        except:
            pass
        self.assertEqual(content, 'c\nb\na')
    
    # overflow line insert
    @patch('builtins.input', side_effect=['load test.md', 'insert a', 'insert 3 b', 'save', 'quit'])
    def test_insert_5(self, input):
        with patch('sys.stdout', new=StringIO()) as output:
            main.run()

        with open('test.md', 'r') as f:
            content = f.read()
        try:
            os.remove('test.md')
        except:
            pass
        self.assertEqual(content, 'a\nb')
    
    # insert line to existing file
    @patch('builtins.input', side_effect=['load test.md', 'insert a', 'save', 'load test.md', 'insert 1 b', 'save', 'quit'])
    def test_insert_6(self, input):
        with patch('sys.stdout', new=StringIO()) as output:
            main.run()

        with open('test.md', 'r') as f:
            content = f.read()
        try:
            os.remove('test.md')
        except:
            pass
        self.assertEqual(content, 'b\na')

    # append head once
    @patch('builtins.input', side_effect=['load test.md', 'append-head a', 'save', 'quit'])
    def test_append_head_1(self, input):
        with patch('sys.stdout', new=StringIO()) as output:
            main.run()

        with open('test.md', 'r') as f:
            content = f.read()
        try:
            os.remove('test.md')
        except:
            pass
        self.assertEqual(content, 'a')
    
    # append head twice
    @patch('builtins.input', side_effect=['load test.md', 'append-head a', 'append-head b', 'save', 'quit'])
    def test_append_head_2(self, input):
        with patch('sys.stdout', new=StringIO()) as output:
            main.run()

        with open('test.md', 'r') as f:
            content = f.read()
        try:
            os.remove('test.md')
        except:
            pass
        self.assertEqual(content, 'b\na')
    
    # append head once
    @patch('builtins.input', side_effect=['load test.md', 'insert a', 'append-head b', 'save', 'quit'])
    def test_append_head_3(self, input):
        with patch('sys.stdout', new=StringIO()) as output:
            main.run()

        with open('test.md', 'r') as f:
            content = f.read()
        try:
            os.remove('test.md')
        except:
            pass
        self.assertEqual(content, 'b\na')
    



if __name__ == '__main__':
    unittest.main()

