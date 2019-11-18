#!/bin/bash

if [ "$#" -ne "3" ]; then
	echo "Usage: $0 <Project Name> <Test Name> <Binary Dir>"
	exit 1
fi

PROJ_NAME=$1
BIN_DIR=$2

${BIN_DIR}/${PROJ_NAME} | tee ${BIN_DIR}/${PROJ_NAME}_results_raw.test
# ruby ${BIN_DIR}/unity-src/auto/parse_output.rb -xml ${BIN_DIR}/${PROJ_NAME}_results_raw.test
# mv report.xml ${BIN_DIR}/${PROJ_NAME}_results.xml