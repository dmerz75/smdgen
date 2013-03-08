#!/bin/bash
# rsync steele

function rsy {
    rsync -avh $1 $2
 }
function sc {
    scp -r $1 $2
 }
echo $1
CURRENT=`pwd`

D=dmerz3@tg-steele.purdue.teragrid.org:/scratch/scratch96/d/dmerz3/valiant/steele/01.da/
S=$CURRENT/$1
sc $S $D
