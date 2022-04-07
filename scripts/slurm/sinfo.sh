#!/bin/bash
ssh -o StrictHostKeyChecking=no $USER@$HEAD '
sinfo --noheader -h -e -o "%P,%A,%D,%c,%m,%C,%G"|awk -F"," "{ split(\$2,alloc,\"/\"); split(\$6,cpus,\"/\"); print \"allocation,partition=\" \$1 \" allocated=\" alloc[1] \",idle=\" alloc[2] \",total=\" \$3 \",unavailable=\" \$3-alloc[2]-alloc[1] \",cpu=\" \$4 \",mem=\" \$5 \",cpu_allocated=\" cpus[1] \",cpu_idle=\" cpus[2] \",other=\" cpus[3] \",cpu_total=\" cpus[4]}"
'
