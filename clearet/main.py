import platform
import logging
import sys

import fileutils
import defaultcfgparser
import datafileparser
from retentionfile import RetentionFile

# TODO: Multiple directories in config file

log_format = "%(asctime)s %(levelname)s [%(module)s] %(message)s"
files_read = []
retention_files = []
configuration_file = "../conf/clearet.ini"
log_file = "../log/clearet.log"
is_changed = False

log_file_path = fileutils.get_absolute_path(
    __file__,
    log_file)
configuration_file_path = fileutils.get_absolute_path(
    __file__,
    configuration_file)

try:
    logging.basicConfig(
        format=log_format,
        filename=log_file_path,
        level=logging.INFO)
except OSError:
    print("Log directory does not exist.")
    sys.exit(1)

logging.info("Running on " + platform.system() + " " + platform.processor())
logging.info("Using Python " + platform.python_version())

configuration = defaultcfgparser.parse(configuration_file_path)
data_file = defaultcfgparser.get_data_file(configuration)
logging.info("Using DataFile " + data_file)
directory = defaultcfgparser.get_directory(configuration)
logging.info("Searching files in directory " + directory)
retention_periods = defaultcfgparser.get_retention_periods(configuration)
logging.info("Using retention periods " + str(retention_periods))

if fileutils.check_file_exists(data_file):
    logging.info("Reading files from DataFile")
    retention_files = datafileparser.load_data(data_file)
    for retention_file in retention_files:
        files_read.append(retention_file.file)

files_current = fileutils.get_all_files(directory, retention_periods)

for file in files_current:
    if not files_read or file not in files_read:
        retention_files.append(RetentionFile(
            file,
            fileutils.get_creation_time(file),
            fileutils.get_expiration_time(file, retention_periods)))
        is_changed = True
        logging.info("Adding new file " + file + " to DataFile")

retention_files_tmp = retention_files[:]

for retention_file in retention_files_tmp:
    if fileutils.remove_file(retention_file):
        retention_files.remove(retention_file)
        logging.info(
            "Removing file " + retention_file.file
            + " from DataFile and directory")
        is_changed = True

if is_changed:
    logging.info("Writing files to DataFile")
    datafileparser.save_data(data_file, retention_files)

sys.exit(0)
