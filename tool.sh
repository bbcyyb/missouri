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
    echo -e "-u, --upgrade      upgrade database"
    echo -e "-r, --reset        reset development environment"
    exit 1
}

environment() {
    echo -e "${SKYBLUE}=======> start to display current environent variables${EOS}"
    echo -e "MAIL_USERNAME=${MAIL_USERNAME}"
    echo -e "MAIL_PASSWORD=${MAIL_PASSWORD}"
    echo -e "MISSOURI_ADMIN=${MISSOURI_ADMIN}"

}

cleanup() {
    DB_FILE=data-dev.sqlite
    echo -e "${SKYBLUE}=======> start to clean database${EOS}"
    if [ -f "$DB_FILE" ]
    then
        rm -rf $DB_FILE
        echo -e "${GREEN}delte database file $DB_FILE successfully${EOS}"
    else
        echo -e "${YELLOW}do not find ${DB_FILE}${EOS}"
    fi
}

upgrade() {
    echo -e "${SKYBLUE}=======> start to upgrade development environment${EOS}"
    python missouri.py db upgrade
}

reset() {
    cleanup
    upgrade
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
        -u | --upgrade)
            upgrade
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