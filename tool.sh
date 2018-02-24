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
EOC=\\033[0m

usage() {
    echo -e "usage: $0 [option...]"
    echo
    echo -e "where"
    echo -e "--help         display help info"
    echo -e "--environent   display current environent variables"
    echo -e "--clean        clean all database, rollback to initial state"
    echo -e "--deploy       deploy new env"
    echo -e "--reset        reset development environment"
    echo -e "--build        build a docker image"
    exit 1
}

environment() {
    echo -e "=======> start to ${SKYBLUE}display${EOC} current environent variables"
    echo -e "MAIL_USERNAME=${MAIL_USERNAME}"
    echo -e "MAIL_PASSWORD=${MAIL_PASSWORD}"
    echo -e "MISSOURI_ADMIN=${MISSOURI_ADMIN}"

}

cleanup() {
    DB_FILE=data-dev.sqlite
    MIGRATIONS_FOLDER=migrations/
    echo -e "=======> start to ${SKYBLUE}cleanup${EOC}"

    if [[ -d "$MIGRATIONS_FOLDER" ]]
    then
        rm -rf $MIGRATIONS_FOLDER
        echo -e "${GREEN}delte ${MIGRATIONS_FOLDER} successfully${EOC}"
    else
        echo -e "${YELLOW}do not find ${MIGRATIONS_FOLDER}${EOC}"
    fi

    if [[ -f "$DB_FILE" ]]
    then
        rm -rf $DB_FILE
        echo -e "${GREEN}delte database file ${DB_FILE} successfully${EOC}"
    else
        echo -e "${YELLOW}do not find ${DB_FILE}${EOC}"
    fi
}

deploy() {
    echo -e "=======> start to ${SKYBLUE}deploy${EOC} development environment"
    python src/missouri.py deploy
}

reset() {
    cleanup
    deploy 
}

build() {
    echo -e "=======> start to ${SKYBLUE}build missouri docker image${EOC}"
    docker build -t missouri:latest .
}

run() {
    echo -e "=======> start to ${SKYBLUE}run missouri docker image${EOC}"
    docker run missouri:latest
}

[[ $# -eq 0 ]] && usage

while [[ $# -gt 0 ]]; do
    case $1 in
        --help)
            usage
            shift 1
            ;;
        --environment)
            environment
            shift 1
            ;;
        --cleanup)
            cleanup
            shift 1
            ;;
        --deploy)
            deploy 
            shift 1
            ;;
        --reset)
            reset
            shift
            ;;
        --build)
            build
            shift 1
            ;;
        --run)
            run
            shift 1
            ;;
        *)
            usage
            shift 1
            ;;
    esac
done
