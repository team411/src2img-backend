#!/bin/bash -x

set -e

tools/build.sh

version=`tools/increment-version.py`

git tag $version
cd frontend && git tag $version && cd ..

tar czf ../src2img.$version.tar.gz .
