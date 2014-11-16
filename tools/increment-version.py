#!/usr/bin/env python2

import subprocess
import sys

p = subprocess.Popen('git tag', shell=True, stdout=subprocess.PIPE)
stdout, err = p.communicate()

if err is not None:
    raise err

versions = []
for line in stdout.split('\n'):
    try:
        epoch, major, minor = line.strip().split('.')
        versions.append((int(epoch), int(major), int(minor),))
    except Exception:
        pass

s_versions = sorted(versions)
if len(s_versions) > 0:
    v = list(s_versions[-1])
    v[-1] = v[-1] + 1
    sys.stdout.write('.'.join(map(str, v)))
else:
    sys.stdout.write('0.0.1')
