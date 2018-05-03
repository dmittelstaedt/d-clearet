import platform
import fileutils
import defaultcfgparser
from retentionfile import RetentionFile

print(platform.python_version())

# TODO: Print statements in log file
# TODO: Multiple directories in config file

files_read = []
retention_files = []
configuration_file = "conf/clearet.ini"

configuration_file_path = fileutils.get_absolute_path(
    __file__,
    configuration_file)

configuration = defaultcfgparser.parse(configuration_file_path)
data_file = defaultcfgparser.get_data_file(configuration)
directory = defaultcfgparser.get_directory(configuration)
retention_periods = defaultcfgparser.get_retention_periods(configuration)
print(data_file)
print(directory)
print(retention_periods)

if fileutils.check_file_exists(data_file):
    retention_files = fileutils.load_data(data_file)
    for retention_file in retention_files:
        files_read.append(retention_file.file)

files_current = fileutils.get_all_files(directory, retention_periods)

for file in files_current:
    if not files_read or file not in files_read:
        retention_files.append(RetentionFile(
            file,
            fileutils.get_creation_time(file),
            fileutils.get_expiration_time(file, retention_periods)))

retention_files_tmp = retention_files[:]

for retention_file in retention_files_tmp:
    if fileutils.remove_file(retention_file):
        retention_files.remove(retention_file)

fileutils.save_data(data_file, retention_files)
