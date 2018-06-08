import unittest
from clearet import defaultcfgparser
from clearet import fileutils


class TestDefaultCfgParser(unittest.TestCase):
    """Class for testing the functions from the defaultcfgparser"""

    @classmethod
    def setUpClass(cls):
        """Doing the set up for the test cases in this class. The configuration
        will be loaded from the given configuration file.
        """
        configuration_file = "conf/clearet-test.ini"
        configuration_file_path = fileutils.get_absolute_path(
            __file__,
            configuration_file)
        cls.configuration = defaultcfgparser.parse(configuration_file_path)

    def test_get_data_file(self):
        """Tests if the parameter of the data file is loaded correctly from the
        configuration file.
        """
        expected_data_file = "/home/user/d-clearet/var/data.csv"
        data_file = defaultcfgparser.get_data_file(self.configuration)
        self.assertEqual(expected_data_file, data_file)

    def test_get_directory(self):
        """Tests if the parameter of the direcotry is loaded correctly from the
        configuration file.
        """
        expected_directory = "/home/user/share"
        directory = defaultcfgparser.get_directory(self.configuration)
        self.assertEqual(expected_directory, directory)

    def test_get_retention_time(self):
        """Tests if the parameter of the retention time for the print files is
        loaded correctly from the configuration file.
        """
        prt_retention_time = defaultcfgparser.get_retention_time(
            self.configuration)
        self.assertEqual(28, prt_retention_time)


if __name__ == "__main__":
    unittest.main()
