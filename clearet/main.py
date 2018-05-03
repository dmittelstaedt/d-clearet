import platform
import file_helper
import configuration
from file_info import FileInfo

print(platform.python_version())

# TODO: Print statements in log file
# TODO: Multiple directories in config file

files_read = []
files_current = []
file_infos = []
configuration_file = "conf/clearet.ini"

configuration_file_path = file_helper.get_absolute_path(
    __file__,
    configuration_file)

parsed_configuration = configuration.parse(configuration_file_path)
data_file = configuration.get_data_file(parsed_configuration)
directory = configuration.get_directory(parsed_configuration)
retention_periods = configuration.get_retention_periods(parsed_configuration)
print(data_file)
print(directory)
print(retention_periods)

if file_helper.check_file_exists(data_file):
    file_infos = file_helper.load_data(data_file)
    for file_info in file_infos:
        files_read.append(file_info.file)

files_current = file_helper.get_all_files(directory, retention_periods)

for file in files_current:
    if not files_read or file not in files_read:
        file_infos.append(FileInfo(
            file,
            file_helper.get_creation_time(file),
            file_helper.get_expiration_time(file, retention_periods)))

file_infos_tmp = file_infos[:]

for file_info in file_infos_tmp:
    if file_helper.remove_file(file_info):
        file_infos.remove(file_info)

file_helper.save_data(data_file, file_infos)
