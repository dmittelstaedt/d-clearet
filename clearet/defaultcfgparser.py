import configparser


def parse(configuration_file):
    """Parse given configuration file. The file must be in ini-format"""
    configuration = configparser.ConfigParser()
    configuration.read(configuration_file)
    return configuration


def get_data_file(configuration):
    """Get datafile from parsed configuration"""
    file = configuration['file']
    return file['datafile']


def get_directory(configuration):
    """Get directory from parsed configuration"""
    directory = configuration['directory']
    return directory['directory']


def get_retention_time(configuration):
    """Returns the retention time for prt files from configuration file"""
    prt_retention_time = configuration['prt_retention_time']
    return int(prt_retention_time['duration'])


def get_retention_periods(configuration):
    """Get retention periods from parsed configuration"""
    retention_periods = {}
    retention = configuration['retention']
    for key in retention:
        retention_periods[key] = int(retention[key])
    return retention_periods
