import os
import datetime


def get_absolute_path(current_file, configuration_file):
    """Return absolute path from current file and relative path
    to the configuration file
    """
    current_path = os.path.abspath(os.path.dirname(current_file))
    return os.path.join(current_path, configuration_file)


def get_directories(root_directory):
    """Return a tuple with directories which contain either prt or wrk
    directories.
    """
    prt_directories = []
    wrk_directories = []
    for root, dirs, files in os.walk(root_directory):
        for dir in dirs:
            if dir == 'prt':
                prt_directories.append(os.path.join(root, dir))
            if dir == "wrk":
                wrk_directories.append(os.path.join(root, dir))
    return prt_directories, wrk_directories


def get_wrk_files(wrk_directories, retention_periods):
    """Return all files from given directories and retention periods"""
    wrk_files = []
    for wrk_directory in wrk_directories:
        files = os.listdir(wrk_directory)
        for file in files:
            wrk_file = os.path.join(wrk_directory, file)
            retention_period = get_retention_period(wrk_file)
            if (retention_period in retention_periods
                    and check_file_exists(wrk_file)):
                wrk_files.append(wrk_file)
    return wrk_files


def get_prt_files(prt_directories):
    """Return all print files from given directories"""
    prt_files = []
    for prt_directory in prt_directories:
        files = os.listdir(prt_directory)
        for file in files:
            prt_file = os.path.join(prt_directory, file)
            if check_file_exists(prt_file):
                prt_files.append(prt_file)
    return prt_files


def get_retention_period(file):
    """Return the retention period from file name"""
    filename, file_ext = os.path.splitext(file)
    return file_ext[1:]


def get_creation_time(file):
    """Return the creation time of a file"""
    return datetime.datetime.fromtimestamp(os.path.getmtime(file))


# TODO: Don't return None
def get_expiration_time(file, duration=0, retention_periods=[]):
    """Return the calculated resting time from file name"""
    if not retention_periods:
        dt_mod = get_creation_time(file)
        dt_ret = dt_mod + datetime.timedelta(days=+duration)
    else:
        ret_period = get_retention_period(file)
        if ret_period in retention_periods:
            if (retention_periods[ret_period] == -1):
                dt_ret = retention_periods[ret_period]
            else:
                dt_mod = get_creation_time(file)
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
