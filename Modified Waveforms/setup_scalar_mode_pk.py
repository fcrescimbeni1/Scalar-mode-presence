#!/usr/bin/env python
"""
setup.py file
"""

from setuptools import Extension, setup, Command
from setuptools import find_packages

VERSION = '0.0.dev0'

setup (
    name = 'pycbc-pk_SD',
    version = VERSION,
    description = 'Waveform plugin for PyCBC modified Ringdown Waveform',
    #long_description = open('descr.rst').read(),
    author = 'The PyCBC team',
    author_email = 'francesco.crescimbeni@gmail.com',
    #url = 'http://www.pycbc.org/',
    #download_url = 'https://github.com/gwastro/revchirp/tarball/v%s' % VERSION,
    keywords = ['pycbc', 'signal processing', 'gravitational waves'],
    install_requires = ['pycbc'],
    py_modules = ['Ringdown_plus_scalar_mode_generic_overtone'],
    entry_points = {"pycbc.waveform.td":"TdQNMfromFinalMassSpin_SD_pk = Ringdown_plus_scalar_mode_pk:TdQNMfromFinalMassSpin_SD_pk"},
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Intended Audience :: Science/Research',
        'Natural Language :: English',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Astronomy',
        'Topic :: Scientific/Engineering :: Physics',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    ],
)
