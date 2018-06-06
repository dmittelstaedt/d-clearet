import platform
import logging

import fileutils
import defaultcfgparser
import datafileparser
from retentionfile import RetentionFile


class Controller():
    """This class controls the execution of the programm"""

    def __init__(self, log_format, configuration_file, log_file):
        self.log_foramt = log_format
        self.configuration_file = configuration_file
        self.log_file = fileutils.get_absolute_path(__file__, log_file)
        self.configuration_file = fileutils.get_absolute_path(
            __file__, configuration_file)

    def run(self):
        """ Runs the steps for finding new files in the root directory,
        calculating their expiration time and writing these infos to the data
        file. If a data file already exists the infos are read from this file.
        Changes to the data file are only written if new files exists or old
        files are removed.
        """

        files_read = []
        retention_files = []
        is_changed = False

        # Load configuration from file
        configuration = defaultcfgparser.parse(self.configuration_file)
        data_file = defaultcfgparser.get_data_file(configuration)
        directory = defaultcfgparser.get_directory(configuration)
        duration = defaultcfgparser.get_retention_time(configuration)
        retention_periods = defaultcfgparser.get_retention_periods(
            configuration)

        # Initial Logging with infos from the configuration file
        logging.info("Running on " + platform.system() + " "
                     + platform.processor())
        logging.info("Using Python " + platform.python_version())
        logging.info("Using DataFile " + data_file)
        logging.info("Searching files in directory " + directory)
        logging.info("Using retention time: " + str(duration))
        logging.info("Using retention periods " + str(retention_periods))

        # Read information from data file if it exists
        if fileutils.check_file_exists(data_file):
            logging.info("Reading files from DataFile")
            retention_files = datafileparser.load_data(data_file)
            for retention_file in retention_files:
                files_read.append(retention_file.file)

        # Fetch print and work files from given root directory
        prt_directories, wrk_directories = fileutils.get_directories(directory)
        prt_files = fileutils.get_prt_files(prt_directories)
        wrk_files = fileutils.get_wrk_files(wrk_directories, retention_periods)
        files_current = prt_files + wrk_files

        # Create retention file instances for found print and work files.
        # All instances are saved in the same list.
        for file in files_current:
            if not files_read or file not in files_read:
                if file in prt_files:
                    retention_files.append(RetentionFile(
                        file,
                        fileutils.get_creation_time(file),
                        fileutils.get_expiration_time(
                            file,
                            duration=duration)))
                else:
                    retention_files.append(RetentionFile(
                        file,
                        fileutils.get_creation_time(file),
                        fileutils.get_expiration_time(
                            file,
                            retention_periods=retention_periods)))
                is_changed = True
                logging.info("Adding new file " + file + " to DataFile")

        # Make a copy of the list with all retention file instances
        retention_files_tmp = retention_files[:]

        # Removing files which expiration time is older than the current date
        for retention_file in retention_files_tmp:
            if fileutils.remove_file(retention_file):
                retention_files.remove(retention_file)
                logging.info(
                    "Removing file " + retention_file.file
                    + " from DataFile and directory")
                is_changed = True

        # Writing all retention files to the data file if something changed
        if is_changed:
            logging.info("Writing files to DataFile")
            datafileparser.save_data(data_file, retention_files)
