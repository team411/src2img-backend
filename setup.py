#!/usr/bin/env python

from distutils.core import setup

package_name = 'src2img'
package_data = {}
package_data[package_name] = ['VERSION']

__version__ = open(package_name + '/VERSION', 'r').read()

setup(
    name=package_name,
    version=__version__,
    description='Backend for BEM hackathon project',
    author='Dmitry Moskowski',
    author_email='me@corpix.ru',
    url='https://github.com/team411/src2img-backend',
    packages=[
        package_name,
    ],
    scripts=['bin/' + package_name],
    package_data=package_data
)
