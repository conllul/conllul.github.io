#!/bin/bash

set -x
for d in `ls -1d UL*`; do
    echo $d;
    pushd $d/ > /dev/null;
    git branch --set-upstream-to=origin/master master;
    git push --force --set-upstream origin master
    popd > /dev/null;
done
