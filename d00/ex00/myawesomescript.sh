#!/bin/sh

if [ "$#" -eq 1 ] && ([[ "$1" == "https://bit.ly"* ]] || [[ "$1" == "http://bit.ly"* ]] || [[ "$1" == "bit.ly"* ]]); then
    curl -sI $1 | grep -e location -e Location | cut -d ' ' -f2
fi