import unittest
from clearet import defaultcfgparser
from clearet import fileutils


class TestDefaultCfgParser(unittest.TestCase):
    """Class for testing the functions from the defaultcfgparser"""
    configuration = None

    @classmethod
    def setUpClass(cls):
        configuration_file = "../conf/clearet.ini"
        configuration_file_path = fileutils.get_absolute_path(
            __file__,
            configuration_file)
        cls.configuration = defaultcfgparser.parse(configuration_file_path)

    def test_get_retention_time(self):
        prt_retention_time = defaultcfgparser.get_retention_time(
            self.configuration)
        self.assertEqual(28, prt_retention_time)


if __name__ == "__main__":
    unittest.main()
