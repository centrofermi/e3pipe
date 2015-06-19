#!/bin/bash

END_DATE="2014-11-18"
DAYS_SPANNED=23
OUTPUT_FOLDER=~/eeedata

export E3PIPE_RECON_BASE=/recon

for station in \
    CAGL-01 \
    CAGL-02

do
    basename=${OUTPUT_FOLDER}/${station}_full_pilot
    e3merge.py -t full -s ${station} -E ${END_DATE} -N ${DAYS_SPANNED} \
	-o ${basename}.root
done
