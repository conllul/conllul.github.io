#!/bin/bash

set -x
for d in `ls -1d UL*`; do
    echo $d;
    pushd $d/ > /dev/null;
    git push
    popd > /dev/null;
done
