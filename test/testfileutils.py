import unittest
import os
from clearet import fileutils


class TestFileUtils(unittest.TestCase):
    """Class for testing the functions from testutils."""
    tmp_directory = "tmp"

    @classmethod
    def setUpClass(cls):
        print("Start")
        os.makedirs(cls.tmp_directory)

    def test_get_absolute_path(self):
        file_name = "/home/user/test.py"
        config_file_name = "conf/config.ini"
        full_path = "/home/user/conf/config.ini"
        self.assertEqual(fileutils.get_absolute_path(
            file_name,
            config_file_name), full_path)

    def test_get_retention_period(self):
        file_name = "test"
        file_extenstion = "w02"
        file = file_name + "." + file_extenstion
        self.assertEqual(fileutils.get_retention_period(file), file_extenstion)

    def test_check_file_exists(self):
        self.assertTrue(fileutils.check_file_exists(__file__))

    @classmethod
    def tearDownClass(cls):
        print("End")
        os.rmdir(cls.tmp_directory)


if __name__ == "__main__":
    unittest.main()
