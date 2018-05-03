import configparser


def parse(configuration_file):
    configuration = configparser.ConfigParser()
    configuration.read(configuration_file)
    return configuration


def get_data_file(configuration):
    file = configuration['file']
    return file['datafile']


def get_directory(configuration):
    directory = configuration['directory']
    return directory['directory']


def get_retention_periods(configuration):
    retention_periods = {}
    retention = configuration['retention']
    for key in retention:
        retention_periods[key] = int(retention[key])
    return retention_periods
