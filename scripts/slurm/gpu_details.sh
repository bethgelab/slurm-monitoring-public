#!/bin/bash
ssh -o StrictHostKeyChecking=no $USER@$HEAD '
squeue -h -t R -O Partition:30,NumCPUs,tres-per-node|awk "{ print \$1\",\"\$2\",\"\$3}"'
