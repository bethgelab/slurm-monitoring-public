#!/bin/bash
SCRIPT=$(dirname $0)
source $SCRIPT/.env
QBPATHS=`echo $QBPATHS|awk -F '|' '{ s = $1; for (i = 2; i <= NF; i++) s = s "\n"$i; print s; }'`
for path in ${QBPATHS}
do
    full_path=$path/$ACCOUNT/$USER
    account_path=$path/$ACCOUNT
    $SCRIPT/slurm/qb_write_time.sh $full_path $account_path
done