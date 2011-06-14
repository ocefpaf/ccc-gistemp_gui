#!/usr/bin/env python
# $URL$
# $Rev$
#
# setup.py
#
# Filipe Fernandes, 2011-05-29

from distutils.core import setup
from distutils.command.sdist import sdist

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
      packages = ['CCCgistemp','CCCgistemp.code','CCCgistemp.tool'],
      license = 'LICENSE.txt',
      description = """ccc-gistemp is a reimplementation of GISTEMP in Python""",
      long_description = open('readme.txt').read(), # change to capitals
      author = 'Nick Barnes, David Jones',
      author_email = 'ccc-gistemp@climatecode.org',
      url = 'http://code.google.com/p/ccc-gistemp/',
      download_url =
      'http://ccc-gistemp.googlecode.com/files/ccc-gistemp-0.6.1.tar.gz',
      classifiers = filter(None, classifiers.split("\n")),
      platforms = 'any',
      cmdclass = {'build_py': build_py},
      keywords = ['science', 'climate', 'GIS', 'temperature'],
      scripts=['CCCgistemp/tool/ccc-gistemp.py'],
     )
