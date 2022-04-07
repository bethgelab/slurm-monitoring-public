#!/bin/bash
SCRIPT=$(dirname $0)
source $SCRIPT/.env
PATHSARR=`echo $PATHS|awk -F '|' '{ s = $1; for (i = 2; i <= NF; i++) s = s "\n"$i; print s; }'`
$SCRIPT/slurm/sinfo.sh|python3 $SCRIPT/slurm/parse_sinfo.py
$SCRIPT/slurm/sdiag.sh|python3 $SCRIPT/slurm/parse_sdiag.py
$SCRIPT/slurm/node_details.sh|python3 $SCRIPT/slurm/parse_node_details.py
$SCRIPT/slurm/node_state.sh
#$SCRIPT/slurm/squeue.sh|python3 $SCRIPT/slurm/parse_squeue.py
$SCRIPT/slurm/gpu_details.sh|python3 $SCRIPT/slurm/parse_gpu_details.py
# Iterate paths and make infos
for path in ${PATHSARR}
do
	$SCRIPT/slurm/qinfo_quota.sh $path|python3 $SCRIPT/slurm/parse_qinfo_quota.py
done
