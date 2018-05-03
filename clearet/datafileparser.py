import csv
import datetime
from retentionfile import RetentionFile


def save_data(data_file, retention_files):
    """Save all files and dates to .csv file"""
    with open(data_file, "w") as csvfile:
        writer = csv.writer(csvfile)
        for retention_file in retention_files:
            writer.writerow([
                retention_file.file,
                retention_file.creation_date,
                retention_file.expiration_date])


def load_data(data_file):
    """Load all files and dates from .csv file"""
    retention_files = []
    with open(data_file, "r") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            expiration_date = -1
            if row[2] != str(expiration_date):
                expiration_date = datetime.datetime.strptime(
                    row[2],
                    "%Y-%m-%d %H:%M:%S.%f")
            retention_files.append(RetentionFile(
                row[0],
                datetime.datetime.strptime(row[1], "%Y-%m-%d %H:%M:%S.%f"),
                expiration_date
                ))
    return retention_files
