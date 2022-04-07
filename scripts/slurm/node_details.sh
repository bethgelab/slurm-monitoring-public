#!/bin/bash
ssh -o StrictHostKeyChecking=no $USER@$HEAD '
sinfo -Nh -O NodeHost,StateLong,CPUsLoad,Memory,AllocMem,Features:100,Gres:100,GresUsed:100,Reason:50|sort|uniq|awk "{print \$1\",\"\$2\",\"\$3\",\"\$4\",\"\$5\",\"\$6}"'
