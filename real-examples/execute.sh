#!/bin/bash

function execute () {
    python3 login_dos.py -f $1
}

if [ $# -eq 0 ]; then
    EMAIL_FILE='email.txt'
else
    EMAIL_FILE=$1
fi

limit=$(ulimit -n)
if [[ $limit != 1024 ]]; then
	ulimit -n 1024
fi

for ((i=0; i < 100; i++))
do
    execute $EMAIL_FILE
done

