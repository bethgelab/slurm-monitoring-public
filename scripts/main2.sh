#!/bin/bash
SCRIPT=$(dirname $0)
source $SCRIPT/.env
$SCRIPT/slurm/pending_jb_partitions.sh|python3 $SCRIPT/slurm/parse_pending_job_partitions.py
