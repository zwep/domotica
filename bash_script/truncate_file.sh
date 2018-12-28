#!/bin/bash

while [ "$1" != "" ]; do
        case $1 in
        -f | --file )           shift
                                filename=$1
                                ;;
        -n )                    shift
                                n=$1
        esac
        shift
done

tail "-$n" "$filename"
