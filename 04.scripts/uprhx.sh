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

D=dale@rhx.chemistry.gatech.edu:/nethome/dale/valiant
S=$CURRENT/$1
sc $S $D
