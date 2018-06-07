import logging
import sys

from controller import Controller
import fileutils

# TODO: Possibility for a dry-run with argument from command line
# TODO: Check right values in ini-file
# TODO: Multiple directories in config file
# TODO: Exception Handling
# TODO: Check if directory for data exists
# TODO: Better output in logfile

log_format = "%(asctime)s %(levelname)s [%(module)s] %(message)s"
log_file = fileutils.get_absolute_path(
    __file__,
    "../log/clearet.log")
configuration_file = fileutils.get_absolute_path(
    __file__,
    "../conf/clearet.ini")

try:
    logging.basicConfig(
        format=log_format,
        filename=log_file,
        level=logging.INFO)
except OSError:
    print("Log directory does not exist.")
    sys.exit(1)

controller = Controller(log_format, configuration_file, log_file)
controller.run()

sys.exit(0)
