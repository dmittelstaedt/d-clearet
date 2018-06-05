import os
import datetime


def get_absolute_path(current_file, configuration_file):
    """Return absolute path from current file and relative path
    to the configuration file
    """
    current_path = os.path.abspath(os.path.dirname(current_file))
    return os.path.join(current_path, configuration_file)


def get_directories(root_directory):
    """Return directories which contain either prt or wrk directory."""
    directories = []
    for root, dirs, files in os.walk(root_directory):
        for dir in dirs:
            if dir == 'prt' or dir == "wrk":
                directories.append(os.path.join(root, dir))
    return directories


# TODO: Rename to get_wrk_files
def get_all_files(directory, retention_periods):
    """Return all files from given directory"""
    files = []
    for root, directories, filenames in os.walk(directory):
        for filename in filenames:
            file = os.path.join(root, filename)
            retention_period = get_retention_period(file)
            if retention_period in retention_periods:
                files.append(file)
    return files


def get_all_prt_files(directory):
    """Return all print files from given directory"""
    prt_directories = []
    files = []
    for root, dirs, filenames in os.walk(directory):
        for dir in dirs:
            if 'prt' == dir:
                prt_directories.append(os.path.join(root, dir))
    # for prt_directory in prt_directories:
    #     prt_files = os.listdir(prt_directory)
    #     for prt_file in prt_files:
    #         prt_file_path = os.path.join(prt_directory, prt_file)
    #         if check_file_exists(prt_file_path):
    #             files.append(prt_file_path)
    return files


def get_retention_period(file):
    """Return the retention period from file name"""
    filename, file_ext = os.path.splitext(file)
    return file_ext[1:]


def get_creation_time(file):
    """Return the creation time of a file"""
    return datetime.datetime.fromtimestamp(os.path.getmtime(file))


# TODO: Don't return None
def get_expiration_time(file, retention_periods):
    """Return the calculated resting time from file name"""
    ret_period = get_retention_period(file)
    if ret_period in retention_periods:
        if (retention_periods[ret_period] == -1):
            dt_ret = retention_periods[ret_period]
        else:
            dt_mod = datetime.datetime.fromtimestamp(
                os.path.getmtime(file))
            dt_ret = dt_mod + datetime.timedelta(
                days=+retention_periods[ret_period])
    else:
        dt_ret = None
    return dt_ret


def remove_file(retention_file):
    """Remove file with given file name"""
    is_removed = False
    if retention_file.expiration_date != -1:
        time_delta = retention_file.expiration_date - datetime.datetime.now()
        if time_delta.total_seconds() < 0:
            os.remove(retention_file.file)
            is_removed = True
    return is_removed


def check_file_exists(filename):
    """Check whether given file exists and is not empty"""
    return (os.path.isfile(filename) and os.path.getsize(filename) > 0)
