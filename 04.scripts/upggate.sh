#!/bin/bash
# rsync ggate

function rsy {
    rsync -avh $1 $2
 }
function sc {
    scp -r $1 $2
 }
echo $1
CURRENT=`pwd`

D=dmerz3@ggate.chemistry.gatech.edu:/nethome/dmerz3/Documents/valiant/ggate/01.da/
S=$CURRENT/$1
sc $S $D
