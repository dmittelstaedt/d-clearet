import unittest
import os
import shutil
import datetime
from clearet import fileutils


class TestFileUtils(unittest.TestCase):
    """Class for testing the functions from testutils."""

    @classmethod
    def setUpClass(cls):
        """Simulate a possible directory structure containing lib, log, prt,
        vor and wrk directories. Some files are going to be created in these
        subdirectories. These files are needed to run the test functions in
        this class.
        """
        cls.base_dir = "tmp/"
        cls.dirs = {
            "lib_dir": "tmp/a0/lib",
            "log_dir": "tmp/a0/log",
            "prt_dir": "tmp/a0/prt",
            "vor_dir": "tmp/a0/vor",
            "wrk_dir": "tmp/a0/wrk",
        }
        cls.files = [
            "tmp/a0/lib/test-prog.jar",
            "tmp/a0/log/test-prog.log",
            "tmp/a0/prt/A2013.PIPP--01.P01.A1803.SC5AD86",
            "tmp/a0/prt/A2014.PIPP--01.P01.A1803.SC5AD86",
            "tmp/a0/vor/test-vor.txt",
            "tmp/a0/wrk/A2013.PIPP--01.W01.A1803.SC5AD86.w02",
            "tmp/a0/wrk/A2013.PIPP--01.W01.A1803.SC5AD86.m01",
            "tmp/a0/wrk/A2014.PIPP--01.P01.A1803.SC5AD86",
        ]
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
        for key, val in cls.dirs.items():
            if not os.path.isdir(cls.dirs[key]):
                os.makedirs(cls.dirs[key])
        for file in cls.files:
            with open(file, "a") as write_file:
                write_file.write(file + "\n")

    def test_get_absolute_path(self):
        file_name = "/home/user/test.py"
        config_file_name = "conf/config.ini"
        full_path = "/home/user/conf/config.ini"
        self.assertEqual(fileutils.get_absolute_path(
            file_name,
            config_file_name), full_path)

    def test_get_retention_period(self):
        file_name = "tmp/a0/wrk/A2013.PIPP--01.W01.A1803.SC5AD86"
        file_extenstion = "m01"
        file = file_name + "." + file_extenstion
        self.assertEqual(fileutils.get_retention_period(file), file_extenstion)

    def test_check_file_exists(self):
        self.assertTrue(fileutils.check_file_exists(__file__))

    def test_get_directories(self):
        prt_dirs, wrk_dirs = fileutils.get_directories(self.base_dir)
        self.assertEqual(len(prt_dirs), 1)
        self.assertEqual(len(wrk_dirs), 1)

    def test_get_prt_files(self):
        prt_dirs = [self.dirs["prt_dir"]]
        prt_files = fileutils.get_prt_files(prt_dirs)
        self.assertEqual(len(prt_files), 2)

    def test_get_wrk_files(self):
        wrk_dirs = [self.dirs["wrk_dir"]]
        wrk_files = fileutils.get_wrk_files(wrk_dirs, self.retention_periods)
        self.assertEqual(len(wrk_files), 2)

    def test_get_expiration_time_prt(self):
        prt_file = ("tmp/a0/prt/A2013.PIPP--01.P01.A1803.SC5AD86")
        prt_exp_time = fileutils.get_expiration_time(prt_file, duration=28)
        excpected_prt_exp_time = fileutils.get_creation_time(prt_file) + \
            datetime.timedelta(days=+28)
        self.assertEqual(excpected_prt_exp_time, prt_exp_time)

    def test_get_expiration_time_wrk(self):
        wrk_file = ("tmp/a0/wrk/A2013.PIPP--01.W01.A1803.SC5AD86.w02")
        wrk_exp_time = fileutils.get_expiration_time(
            wrk_file, retention_periods=self.retention_periods)
        expected_wrk_expt_time = fileutils.get_creation_time(wrk_file) + \
            datetime.timedelta(days=+14)
        self.assertEqual(expected_wrk_expt_time, wrk_exp_time)

    @classmethod
    def tearDownClass(cls):
        """Remove the created base directory for simulating the needed
        directories and files
        """
        shutil.rmtree(cls.base_dir)
        pass


if __name__ == "__main__":
    unittest.main()
