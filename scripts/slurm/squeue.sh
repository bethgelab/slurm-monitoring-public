#!/bin/bash
ssh -o StrictHostKeyChecking=no $USER@$HEAD '
squeue --noheader -o "%A,%P,%T,%C,%D,%L,%R,%a,%u"'
