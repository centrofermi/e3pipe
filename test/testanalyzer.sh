#!/bin/bash

source ~/env.sh

OUTPUT_FOLDER=~/eeedata
export E3PIPE_TEMP=~/eeetmp

for version in V0 V2.5 V2.7 V3.0 V3.1
do
    export E3_ANALYZER=/opt/eee/bin/EEE_Analyzer_${version}
    e3analyzer.py -s ${version} $1
    mv ${E3PIPE_TEMP}/*.out ${OUTPUT_FOLDER}
done
