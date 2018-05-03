import os
import datetime
import csv
from retentionfile import RetentionFile


def get_absolute_path(current_file, configuration_file):
    """Return absolute path from current file and relative path
    to the configuration file
    """
    current_path = os.path.abspath(os.path.dirname(current_file))
    return os.path.join(current_path, configuration_file)


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


def get_retention_period(file):
    """Return the retention period from file name"""
    filename, file_ext = os.path.splitext(file)
    return file_ext[1:]


def get_creation_time(file):
    """Return the creation time of a file"""
    return datetime.datetime.fromtimestamp(os.path.getmtime(file))


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


def remove_file(file_info):
    """Remove file with given file name"""
    is_removed = False
    if file_info.expiration_date != -1:
        time_delta = file_info.expiration_date - datetime.datetime.now()
        if time_delta.total_seconds() < 0:
            print("Removing file: " + file_info.file)
            os.remove(file_info.file)
            is_removed = True
    return is_removed


def check_file_exists(filename):
    """Check whether given file exists and is not empty"""
    return (os.path.isfile(filename) and os.path.getsize(filename) > 0)


def save_data(data_file, file_infos):
    """Save all files and dates to .csv file"""
    print("Writing to file")
    with open(data_file, "w") as csvfile:
        writer = csv.writer(csvfile)
        for file_info in file_infos:
            writer.writerow([
                file_info.file,
                file_info.creation_date,
                file_info.expiration_date])
    print("Finished writing to file")


def load_data(data_file):
    """Load all files and dates from .csv file"""
    print("Reading from file")
    file_infos = []
    with open(data_file, "r") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            expiration_date = -1
            if row[2] != str(expiration_date):
                expiration_date = datetime.datetime.strptime(
                    row[2],
                    "%Y-%m-%d %H:%M:%S.%f")
            file_infos.append(RetentionFile(
                row[0],
                datetime.datetime.strptime(row[1], "%Y-%m-%d %H:%M:%S.%f"),
                expiration_date
                ))
    return file_infos
