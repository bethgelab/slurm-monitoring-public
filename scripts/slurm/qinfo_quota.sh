#!/bin/bash
ssh -o StrictHostKeyChecking=no $USER@$HEAD '
qinfo quota '"$1"'|awk "{while (getline) {print \$1\",\"\$2\",\"\$8}}"'
