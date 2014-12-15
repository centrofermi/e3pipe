#!/bin/bash

END_DATE="2014-10-20"
DAYS_SPANNED=365

export PYTHONPATH=/opt/eee:$PYTHOPATH
export PATH=/opt/eee/e3pipe/apps:/opt/eee/bin:$PATH

export E3PIPE_TEMP=~/eeetmpSAVO
echo "E3PIPE_TEMP set to " $E3PIPE_TEMP

/opt/eee/e3pipe/apps/e3crawl.py \
    -E ${END_DATE} \
    -N ${DAYS_SPANNED} \
    -r \
    -s SAVO-01 \
    -s SAVO-02

