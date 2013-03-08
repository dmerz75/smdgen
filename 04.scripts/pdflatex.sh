#!/bin/bash
# pdflatex 

FILENAME=tm

pdflatex $FILENAME
bibtex $FILENAME
pdflatex $FILENAME
pdflatex $FILENAME
