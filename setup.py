#!/usr/bin/env python3
#
# Copyright 2021, Deepwave Digital, Inc.
# SPDX-License-Identifier: Commercial

import os
import setuptools
import pkg_resources
import sys
import shutil
from pathlib import Path
import subprocess

_SCRIPT_DIR = Path(__file__).parent.absolute()
_PACKAGE_ROOT = _SCRIPT_DIR.parent
_SERVICE_FILE = _PACKAGE_ROOT / 'gpsd_influx2.service'

assert os.getuid() == 0, 'This script must be executed with sudo privileges'

if sys.version_info < (3, 6):
    sys.exit('Sorry, Python < 3.6 is not supported')

pkg_resources.require(['pip >= 10.0.1'])

with open('requirements.txt') as f:
    required_packages = f.read().splitlines()
print(required_packages)

try:
    setuptools.setup(
        name='gpsd_influx2',
        version='1.0.0',
        python_requires='>=3',
        install_requires=required_packages,
        packages=['gpsd_influx2'],
        license='Commercial',
        long_description=open('README.md').read(),
        entry_points={
            'console_scripts': [
                'gpsd_influx2 = gpsd_influx2.gpsd_influx2:main',
            ]
        },
    )
finally:
    shutil.copy(_SERVICE_FILE, Path('/etc/systemd/system/') / _SERVICE_FILE.name)
    subprocess.Popen(['systemctl', 'daemon-reload'], shell=False)
