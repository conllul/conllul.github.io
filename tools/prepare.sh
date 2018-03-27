#!/bin/bash

set -x
for d in `ls -1d UL*`; do
    echo $d;
    pushd $d/ > /dev/null;
    rm -rf .git/;
    git init .;
    git remote add origin git@github.com:conllul/$d.git;
    git add UDLex* > /dev/null;
    git add '*conllul.bz2';
    git add *.json > /dev/null;
    git commit -m 'Adding initial baseline lexicon and conllul' > /dev/null;
    popd > /dev/null;
done
