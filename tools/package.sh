#!/bin/bash -x

set -e

if [ -z "$1" ]
then
    echo "Usage: $0 installation_path"
    exit 1
fi

tools/build.sh

version=`tools/increment-version.py`

git tag $version
cd frontend && git tag $version && cd ..

cpath=$(pwd | sed 's/\//\\\//g')
dpath=$(echo "$1" | sed 's/\//\\\//g')
find .venv -type f | xargs -I{} perl -p -i -e "s/$cpath/$dpath/gm" '{}'
find .venv -type f -name '*.pyc' | xargs rm -f

tar czf ../src2img.$version.tar.gz .
