#!/usr/bin/env python3

import unittest
from unittest.mock import patch  # , MagicMock
from io import StringIO
import os

from dir_compat import check_all


class TestDirectoryCompatibilityChecker(unittest.TestCase):

    def setUp(self):
        self.test_dir = 'test_directory'
        os.makedirs(self.test_dir, exist_ok=True)

    def tearDown(self):
        os.rmdir(self.test_dir)

    @patch('sys.stdout', new_callable=StringIO)
    def assert_stdout(self, expected_output, mock_stdout):
        check_all(self.test_dir, ['ntfs'])
        self.assertEqual(mock_stdout.getvalue().strip(), expected_output.strip())

    def test_nonexistent_directory(self):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            check_all('nonexistent_directory')
            self.assertIn('isn\'t a directory', mock_stdout.getvalue())

    def test_check_all_ntfs(self):
        expected_output = f"Results of checking {self.test_dir} for compatibility issues with ntfs:\n" \
                          f"Checked 0 directorires and 0 files.\n" \
                          "No issues found."
        self.assert_stdout(expected_output)

    def test_check_all_ext(self):
        return
        expected_output = f"Results of checking {self.test_dir} for compatibility issues with ext4:\n" \
                          f"Checked 0 directorires and 0 files.\n" \
                          "No issues found."
        self.assert_stdout(expected_output)

    def test_check_all_with_issues(self):
        return
        # Create a file with a prohibited symbol
        with open(os.path.join(self.test_dir, 'file/with/symbol.txt'), 'w') as file:
            file.write('test')

        expected_output = f"Results of checking {self.test_dir} for compatibility issues with ntfs:\n" \
                          f"{os.path.join(self.test_dir, 'file/with/symbol.txt')} contains \"/\", which isn't allowed on ntfs"
        self.assert_stdout(expected_output)


if __name__ == '__main__':
    unittest.main()
