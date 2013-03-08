#!/bin/bash
# rsync ggate

function rsy {
    rsync -avh $1 $2
 }
function sc {
    scp -r $1 $2
 }

S=dmerz3@fgate-fs.chemistry.gatech.edu:/nethome/dmerz3/Documents/valiant/fgate/tex_feb18update
D=/home/dale/Documents/md/results
sc $S $D
