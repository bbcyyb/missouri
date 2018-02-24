#!/bin/bash

pushd app/
PYTHONPATH="$(pwd):${PYTHONPATH}"
export PYTHONPATH
PATH="$(pwd):${PATH}"
export PATH
python ./missouri.py dev
popd
