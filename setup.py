#!/usr/bin/env python

from distutils.core import setup
import subprocess
from setuptools.command.install import install
from setuptools.command.develop import develop
import os


def install_deps():
    cmd = [
        'export V8_HOME=`pwd`/../v8',
        'python setup.py build && python setup.py install',
        'tools/build.sh'
    ]
    subprocess.call('sh -c "{0}"'.format(';'.join(cmd)),
                    shell=True, cwd=os.path.join(os.getcwd(), 'vendor/pyv8'))
    subprocess.call('pip install -r requirements.txt', shell=True)


class CustomInstallCommand(install):

    def run(self):
        install_deps()
        install.run(self)


class CustomDevelopCommand(develop):

    def run(self):
        install_deps()
        develop.run(self)

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
    cmdclass={
        'install': CustomInstallCommand,
        'develop': CustomDevelopCommand
    },
    scripts=['bin/' + package_name],
    package_data=package_data
)
