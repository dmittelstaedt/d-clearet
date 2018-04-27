import os
import datetime
import csv


class FileHelper:
    """This class offers functions for operating with files in a given
    directory and given set of retention periods.
    """

    def __init__(self, data_file, retention_periods):
        self.data_file = data_file
        self.retention_periods = retention_periods

    def get_all_files(self, directory):
        """Return all files from given directory"""
        files = []
        for root, directories, filenames in os.walk(directory):
            for filename in filenames:
                file = os.path.join(root, filename)
                retention_period = self.get_retention_period(file)
                if retention_period in self.retention_periods:
                    files.append(file)
        return files

    def get_retention_period(self, file):
        """Return the retention period from file name"""
        filename, file_ext = os.path.splitext(file)
        return file_ext[1:]

    def get_creation_time(self, file):
        """Return the creation time of a file"""
        return datetime.datetime.fromtimestamp(os.path.getmtime(file))

    def get_expiration_time(self, file):
        """Return the calculated resting time from file name"""
        ret_period = self.get_retention_period(file)
        if ret_period in self.retention_periods:
            if (self.retention_periods[ret_period] == -1):
                dt_ret = self.retention_periods[ret_period]
            else:
                dt_mod = datetime.datetime.fromtimestamp(
                    os.path.getmtime(file))
                dt_ret = dt_mod + datetime.timedelta(
                    days=+self.retention_periods[ret_period])
        else:
            dt_ret = None
        return dt_ret

    def check_for_new_files(self, files_old, files_new):
        """Check for new files in given directory"""
        pass

    def remove_file(self, filename):
        """Remove file with given file name"""
        pass

    def save_data(self, file_infos):
        """Save all files and dates to .csv file"""
        print("Writing to file")
        with open(self.data_file, "w") as csvfile:
            writer = csv.writer(csvfile)
            for file_info in file_infos:
                writer.writerow([
                    file_info.file,
                    file_info.creation_date,
                    file_info.expiration_date
                ])
        print("Finished writing to file")

    def load_load(self):
        """Load all files and dates from .csv file"""
        pass
