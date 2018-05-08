#!/bin/bash

YAP=../yap
for lexicon in `find . -name 'UDLex*conllul'`; do
    treebank=`echo $lexicon | cut -d '/' -f 2`
    lex_file=`echo $lexicon | cut -d '/' -f 3`
    lex_name=`echo $lex_file | cut -d '.' -f 1 | cut -d '-' -f 2-`
    echo Applying $lex_file to treebank $treebank
    pushd "$treebank/" > /dev/null
    for tb_file in `ls -1 *conllu`; do
        dict_file=`echo $tb_file | cut -d '-' -f 1`
        file_prefix=`echo $tb_file | cut -d '.' -f 1`
        file_split=`echo $file_prefix | cut -d '-' -f 3`
        printf "\tRunning lexicon-based MA on file %s\n" "$tb_file"
        echo $YAP ma -conllu $tb_file -dict $dict_file-dd.json -udlex $lex_file -format ud -out $file_prefix.$lex_name.conllul ">" $file_split-ma.$lex_name.log
        $YAP ma -conllu $tb_file -dict $dict_file-dd.json -udlex $lex_file -format ud -out $file_prefix.$lex_name.conllul 2> $file_split-ma.$lex_name.log
    done
    popd > /dev/null
done
