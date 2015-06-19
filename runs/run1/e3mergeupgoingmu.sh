#!/bin/bash

END_DATE="2015-04-24"
DAYS_SPANNED=5
OUTPUT_FOLDER=~/eeedata

export E3PIPE_RECON_BASE=/recon

for station in \
    SAVO-01 \
    SAVO-02 \
    SAVO-03 \
    FRAS-02

do
    basename=${OUTPUT_FOLDER}/${station}_full_upgoingmu
    e3merge.py -t full -s ${station} -E ${END_DATE} -N ${DAYS_SPANNED} \
	-o ${basename}.root
done
