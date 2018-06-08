#!/bin/bash
#
# Do some requirement checks and installs the d-clearet utility.
#
# Author: David Mittelstaedt <david.mittelstaedt@dataport.de>
# Date: 2018-06-07

# Set return code to 1
RC=1
PYTHON_EXEC=python3
CURRENT_DIRECTORY="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && cd .. && pwd )"

###########################################################
# Do some requirement checks
# Arguments:
#   None
# Returns:
#   True, if requirements are full filled, otherweise false
###########################################################
pre_req() {
  echo "Checking requirements..."
  pre_req_rc=1
  which $PYTHON_EXEC >/dev/null 2>&1
  if [ $? == 0 ]; then
    pre_req_rc=0
  else
    echo "Python 3 is not installed correctly. Please install Python 3 or set the variable PATH correctly."
    return $pre_req_rc
  fi
  echo "Requierements are fulfilled."
  return $pre_req_rc 
}

###########################################################
# Installs the d-clearet utility
# Arguments:
#   None
# Returns:
#   True, if requirements are full filled, otherweise false
###########################################################
install() {
  install_rc=1
  log_dir=$CURRENT_DIRECTORY/log
  var_dir=$CURRENT_DIRECTORY/var
  echo "Starting installation..."
  if [ ! -d $log_dir ]; then
    mkdir $log_dir
  fi
  if [ ! -d $var_dir ]; then
    mkdir $var_dir
  fi
  install_rc=0
  echo "Finished installation successfully."
  return $install_rc
}

###########################################################
# Run the test to verify the correct installation
# Arguments:
#   None
# Returns:
#   True, if all tests ran correctly, otherwise false 
###########################################################
run_tests() {
  run_tests_rc=1
  echo "Running tests..."
  cd $CURRENT_DIRECTORY
  $PYTHON_EXEC -m unittest discover test >/dev/null 2>&1
  run_tests_rc=$?
  if [ $run_tests_rc == 0 ]; then
    echo "Finished running tests successfully."
  else
    echo "An error occuered during running the tests."
  fi
  return $run_tests_rc
}

pre_req
RC=$?
if [ $RC != 0 ]; then
  exit $RC
fi

install
RC=$?
if [ $RC != 0 ]; then
  exit $RC
fi

run_tests
RC=$?
exit $RC
