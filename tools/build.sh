#!/bin/bash -x

set -e
export YENV=production

git clone -b master git@github.com:team411/src2img.git frontend || true
make -C frontend build

rm -rf assets
mkdir assets

for f in `find frontend/desktop.bundles -type f -name '*.bemjson.freeze.js'`
do
    cp -f $f assets/$(echo $f | \
        python -c "import sys,os;sys.stdout.write(os.path.basename(sys.stdin.read()).split('.')[0])").bem.json
done

for f in `find frontend/desktop.bundles -type f | grep -P '\/[a-z0-9-]+\.bemhtml\.js$'`
do
    cp -f $f assets/
done

rm -rf pub/_
cp -r frontend/_ pub/
