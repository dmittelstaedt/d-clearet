import configparser

ini_file = "/home/david/Projects/test-share/clearet.ini"


def parse():
    configuration = configparser.ConfigParser()
    configuration.read(ini_file)
    return configuration


def get_retention_periods(configuration):
    retention_periods = {}
    retention = configuration['retention']
    for key in retention:
        retention_periods[key] = int(retention[key])
    return retention_periods


def get_data_file(configuration):
    file = configuration['file']
    return file['datafile']
