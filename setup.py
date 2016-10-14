# coding: utf-8

import os
import sys

from setuptools import setup

if sys.version_info[0] < 3:
    from io import open


__here__ = os.path.abspath(os.path.dirname(__file__))


def split_requirements(lines):
    requirements, dependencies = [], []

    for line in lines:
        if line.startswith('-e'):
            line = line.split(' ', 1)[1]
            dependencies.append(line)
            line = line.split('#egg=', 1)[1]

        requirements.append(line)

    return requirements, dependencies


with open(os.path.join(__here__, 'requirements', 'dist.txt'), encoding="utf8") as f:
    REQUIREMENTS = [x.strip() for x in f]
    REQUIREMENTS = [x for x in REQUIREMENTS if x and not x.startswith('#')]
    REQUIREMENTS, DEPENDENCIES = split_requirements(REQUIREMENTS)


README = open(os.path.join(__here__, 'README.rst'), encoding="utf8").read()


setup(
    name='il2fb-regiments',
    version='1.0.0',
    description="Access regiments of IL-2 Forgotten Battles flight simulator.",
    long_description=README,
    keywords=[
        'il2', 'il-2', 'fb', 'forgotten battles', 'regiments',
    ],
    license='LGPLv3',
    url='https://github.com/IL2HorusTeam/il2fb-regiments',
    author='Alexander Oblovatniy',
    author_email='oblovatniy@gmail.com',
    packages=[
        'il2fb.regiments',
    ],
    namespace_packages=[
        'il2fb',
    ],
    include_package_data=True,
    install_requires=REQUIREMENTS,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development :: Libraries',
    ],
    platforms=[
        'any',
    ],
)