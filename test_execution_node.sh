#!/bin/bash

param=$1

if [ -z ${param} ]; then
    param=NULL
fi
tstart=$(date +"%H:%M:%S")
sleep 10
tend=$(date +"%H:%M:%S")
echo -e "TESTOUTPUT\t`hostname`\t${param}\t${tstart}\t${tend}"


