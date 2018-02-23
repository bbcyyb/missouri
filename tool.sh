#!/bin/bash

#
# Private a series of functions as tool for development and testing. 
#
# tool.sh <cmd_name>
#

RED=\\033[31m
GREEN=\\033[32m
YELLOW=\\033[33m
BLUE=\\033[34m
SKYBLUE=\\033[36m
EOS=\\033[0m

usage() {
    echo -e "usage: $0 [option...]"
    echo
    echo -e "where"
    echo -e "-h, --help         display help info"
    echo -e "-e, --environent   display current environent variables"
    echo -e "-c, --clean        clean all database, rollback to initial state"
    echo -e "-d, --deploy       deploy new env"
    echo -e "-r, --reset        reset development environment"
    exit 1
}

environment() {
    echo -e "=======> start to ${SKYBLUE}display${EOS} current environent variables"
    echo -e "MAIL_USERNAME=${MAIL_USERNAME}"
    echo -e "MAIL_PASSWORD=${MAIL_PASSWORD}"
    echo -e "MISSOURI_ADMIN=${MISSOURI_ADMIN}"

}

cleanup() {
    DB_FILE=data-dev.sqlite
    echo -e "=======> start to ${SKYBLUE}clean${EOS} database"
    if [ -f "$DB_FILE" ]
    then
        rm -rf $DB_FILE
        echo -e "${GREEN}delte database file $DB_FILE successfully${EOS}"
    else
        echo -e "${YELLOW}do not find ${DB_FILE}${EOS}"
    fi
}

deploy() {
    echo -e "=======> start to ${SKYBLUE}deploy${EOS} development environment"
    python missouri.py deploy
}

reset() {
    cleanup
    deploy 
}

[ $# -eq 0 ] && usage

while [ $# -gt 0 ]; do
    case $1 in
        -h | --help)
            usage
            shift 1
            ;;
        -e | --environment)
            environment
            shift 1
            ;;
        -c | --cleanup)
            cleanup
            shift 1
            ;;
        -d | --deploy)
            deploy 
            shift 1
            ;;
        -r | --reset)
            reset
            shift
            ;;
        *)
            usage
            shift 1
            ;;
    esac
done
