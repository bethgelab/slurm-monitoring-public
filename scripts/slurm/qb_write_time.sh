#!/bin/bash
ssh -o StrictHostKeyChecking=no $USER@$HEAD '
start_time="$(date -u +%s.%N)"
cd '"$1"'
touch a.txt && echo "This is some write text" > a.txt
end_time="$(date -u +%s.%N)"
elapsed="$(bc <<<"$end_time-$start_time")"
echo "qb_write_time,location='"$2"' time_taken=$elapsed"
'
