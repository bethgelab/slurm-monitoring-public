ssh -o StrictHostKeyChecking=no $USER@$HEAD '
sinfo -o "%n,%T" --noheader | awk -F"," "{ if (substr(\$2,length(\$2),1) == \"*\") { RESPONDING=0; STATE=substr(\$2,0,length(\$2)-1) } else { RESPONDING=1;STATE=\$2 } print \"node_state,hostname=\" \$1 \",state=\" STATE \" responding=\" RESPONDING }"
'