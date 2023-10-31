import unittest
from unittest.mock import patch
from io import StringIO

import main

output_template = 'Session is over\n'

class TestCLI(unittest.TestCase):
    @patch('builtins.input', side_effect=['quit'])
    def test_history_command(self, input):
        with patch('sys.stdout', new=StringIO()) as output:
            main.run()
        expected_output = '' + output_template
        self.assertIn(expected_output, output.getvalue())


if __name__ == '__main__':
    unittest.main()

