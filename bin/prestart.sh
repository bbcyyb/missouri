#!/usr/bin/env bash

echo "** deploy missouri..."
pushd /src/
python ./missouri.py deploy
popd
