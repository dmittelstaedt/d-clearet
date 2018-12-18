d-clearet
==============

A little tool for removing files based on their retention period. The retention period is given via the extension of the file.

Requirements
--------------

- Remove files in an directory and its subdirectories
- Print files are located in subdirectories called prt. Print files don't have a retention period. They will be removed after a fixed time of their creation.
- Work files are located in subdirectories called wrk. Work files have a retention period. The retention period is given via the extension of the file. The files can have more than one dot in their filenames. The files will be removed accordingly to their retention period.
- The time stamp of the creation of the file is base for removing files. Access and change time stamps of the files are not used for the calculation.

Features
--------------

- Saving all files from given directory in a CSV-file.
- Loading all files from a given CSV-file.
- Removing all print and work files based on their time stamp or retention period.

System Requirements
--------------

- Python 3 has to be installed on the target system.

Installation
--------------

- Clone the repository and checkout the stable branch.
- Run the installation script install.sh from the bin directory. This script checks the necessary requirements, installs the tool and runs some tests.

Usage
--------------

- Configure the tool with the configuration file from the conf directory. This file is in INI-format. The directory, where the tool searches the files, the file, where the information to the found files will be hold, the retention time for print files and the retention time for work files can be configured.
- Run the script clearet from the bin directory to start this tool.
- The output goes in a log file, which is located in the ./log directory.
