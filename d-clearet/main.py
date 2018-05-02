import platform
from file_helper import FileHelper
from file_info import FileInfo

print(platform.python_version())

# TODO: Check wether new files are in the directory (mtime during running is
# the the creation time)
# TODO: Load file names and relevant dates in .csv file
# TODO: Remove expired files
# TODO: Create config file

directory = "/home/david/Projects/test-share"
data_file = "/home/david/Projects/test-share/data.csv"
file_infos = []

retention_periods = {
    "w02": 14,
    "j01": 365,
    "j02": 730,
    "j10": 3650,
    "m01": 30,
    "m02": 60,
    "m03": 93,
    "m04": 120,
    "m06": 180,
    "m18": 540,
    "nol": -1,
    "od1": -1
}

file_helper = FileHelper(data_file, retention_periods)
# file_helper.save_data()
files = file_helper.get_all_files(directory)
# print (len(files))
#
for file in files:
    print(file)
    file_infos.append(FileInfo(
        file,
        file_helper.get_creation_time(file),
        file_helper.get_expiration_time(file)))

print(len(file_infos))
file_helper.save_data(file_infos)
