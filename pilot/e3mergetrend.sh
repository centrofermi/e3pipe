#!/bin/bash

END_DATE="2014-11-14"
DAYS_SPANNED=19 
OUTPUT_FOLDER=~/eeedata

for station in \
    ALTA-01 \
    BARI-01 \
    BOLO-03 \
    CAGL-01 \
    CAGL-02 \
    CAGL-03 \
    CATA-02 \
    CATZ-01 \
    FRAS-02 \
    GROS-01 \
    LAQU-01 \
    LAQU-02 \
    LECC-01 \
    LECC-02 \
    LODI-01 \
    PISA-01 \
    SAVO-01 \
    SAVO-02 \
    TORI-04 \
    TRAP-01 \
    TRIN-01 \
    VIAR-01 \
    VIAR-02
do
    basename=${OUTPUT_FOLDER}/${station}-trending-pilot
    e3merge.py -t trending -s ${station} -E ${END_DATE} -N ${DAYS_SPANNED} \
	-o ${basename}.root
    e3root2text.py -t Header ${basename}.root
    e3root2text.py -t Weather ${basename}.root
    e3root2text.py -t Trending ${basename}.root
done
