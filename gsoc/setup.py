#!/usr/bin/env python
# $URL$
# $Rev$
#
# setup.py
#
# Filipe Fernandes, 2011-05-29

import os
from distutils.core import setup
from distutils.command.sdist import sdist
#import py2exe

try: # Python 3
  from distutils.command.build_py import build_py_2to3 as build_py
except ImportError: # Python 2
  from distutils.command.build_py import build_py

classifiers = """\
Development Status :: 5 - Production/Stable
Environment :: Console
Intended Audience :: Science/Research
Intended Audience :: Developers
Intended Audience :: Education
License :: OSI Approved :: BSD License
Operating System :: OS Independent
Programming Language :: Python
Topic :: Scientific/Engineering
Topic :: Education
Topic :: Software Development :: Libraries :: Python Modules
"""

setup(name = 'ccc-gistemp',
      version = '0.6.1',
      packages = ['code','tool'],
      # pack some data for a example run?
      # also, where to save the data?
      #license = 'LICENSE.txt', #TODO: Add a separate with the copyright msg
      summary = 'Clear Climate Code GISTEMP project',
      description = """
ccc-gistemp is a reimplementation of GISTEMP in Python for clarity. GISTEMP is
a reconstruction of the global historical temperature record from land and sea
surface temperature records. It produces a familiar graph of historical
temperatures
      """,
      long_description = open('readme.txt').read(), # change to capitals
      author = 'Nick Barnes, David Jones',
      author_email = 'gsoc-2011@climatecode.org', #TODO: add a real email
      #maintainer = '', 
      #maintainer_email = '',
      url = 'http://code.google.com/p/ccc-gistemp/',
      #url = 'http://pypi.python.org/pypi/ccc-gistemp/', #TODO: register at pypi
      #download_url = 'http://pypi.python.org/packages/source/x/ccc-gistemp/', #TODO: register at pypi
      classifiers = filter(None, classifiers.split("\n")),
      platforms = 'any',
      cmdclass = {'build_py': build_py},
      keywords = ['science', 'climate', 'GIS', 'temperature'], #TODO: are these #OK?
     )
