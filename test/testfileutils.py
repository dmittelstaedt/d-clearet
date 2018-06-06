import unittest
import os
import datetime
from clearet import fileutils


class TestFileUtils(unittest.TestCase):
    """Class for testing the functions from testutils."""
    tmp_directory = "tmp"
    retention_periods = {}

    @classmethod
    def setUpClass(cls):
        cls.retention_periods = {
            "w02": 14,
            "j01": 365,
            "j02": 730,
            "j10": 3650,
            "m01": 30,
            "m02": 60,
            "m03": 93,
            "m04": 120,
            "m06": 180,
            "m18": 540,
            "nol": -1,
            "od1": -1
        }
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

    def test_get_directories(self):
        prt_dirs, wrk_dirs = fileutils.get_directories(
            "/home/david/Projects/test-share")
        self.assertEqual(len(prt_dirs), 2)
        self.assertEqual(len(wrk_dirs), 2)

    def test_get_prt_files(self):
        prt_dirs = [
            "/home/david/Projects/test-share/a0/prt",
            "/home/david/Projects/test-share/a1/prt"]
        prt_files = fileutils.get_prt_files(prt_dirs)
        self.assertEqual(len(prt_files), 7)

    def test_get_wrk_files(self):
        wrk_dirs = [
            "/home/david/Projects/test-share/a0/wrk",
            "/home/david/Projects/test-share/a1/wrk"]
        wrk_files = fileutils.get_wrk_files(wrk_dirs, self.retention_periods)
        self.assertEqual(len(wrk_files), 8)

    def test_get_expiration_time(self):
        prt_file = (
            "/home/david/Projects/test-share/a0/prt/A2013.PIPP--"
            "01.P01.A1803.SC5AD86")
        wrk_file = (
            "/home/david/Projects/test-share/a0/wrk/A2013.PIPP--"
            "01.W01.A1803.SC5AD86.w02")
        prt_exp_time = fileutils.get_expiration_time(prt_file, duration=28)
        wrk_exp_time = fileutils.get_expiration_time(
            wrk_file, retention_periods=self.retention_periods)
        excpected_prt_exp_time = fileutils.get_creation_time(prt_file) + \
            datetime.timedelta(days=+28)
        expected_wrk_expt_time = fileutils.get_creation_time(wrk_file) + \
            datetime.timedelta(days=+14)
        self.assertEqual(excpected_prt_exp_time, prt_exp_time)
        self.assertEqual(expected_wrk_expt_time, wrk_exp_time)

    @classmethod
    def tearDownClass(cls):
        os.rmdir(cls.tmp_directory)


if __name__ == "__main__":
    unittest.main()
