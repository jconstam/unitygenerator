#!/bin/bash

if [ "$#" -ne "3" ]; then
	echo "Usage: $0 <Ruby Script> <YAML Settings File> <Include Path>"
	exit 1
fi

RUBY_SCRIPT=$1
SETTINGS_FILE=$2
INCLUDE_PATH=$3

ruby ${RUBY_SCRIPT} -o${SETTINGS_FILE} ${INCLUDE_PATH}/*.h

for f in ${INCLUDE_PATH}/*; do
    if [ -d ${f} ]; then
		echo "RECURSING INTO ${f} from ${INCLUDE_PATH}"
		source $0 ${RUBY_SCRIPT} ${SETTINGS_FILE} ${f}
	fi
done