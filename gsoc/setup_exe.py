#!/usr/bin/env python
# $URL$
# $Rev$
#
# setup_exe.py
#
# Filipe Fernandes, 2011-06-02

import os
import py2exe
from distutils.core import setup
from distutils.command.sdist import sdist

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

data_files = [('',['readme.txt', 'LICENSE.txt', 'release-notes.txt'])]

setup(name = 'ccc-gistemp',
      version = '0.6.1',
      packages = ['CCCgistemp','CCCgistemp.code','CCCgistemp.tool'],
      console=[{"script": 'CCCgistemp/tool/ccc-gistemp.py',
      "icon_resources": [(1, "world_globe.ico")]}],
      options = {"py2exe": {
                            "compressed":2,
                            "optimize":2,
                            "bundle_files":2,
                            "dist_dir":'dist',
                            "xref":False,
                            "skip_archive":False,
                            "ascii": False,
                            "custom_boot_script":''
                            }},
      license = 'LICENSE.txt',
      description = """
ccc-gistemp is a reimplementation of GISTEMP in Python for clarity. GISTEMP is
a reconstruction of the global historical temperature record from land and sea
surface temperature records. It produces a familiar graph of historical
temperatures
      """,
      long_description = open('readme.txt').read(),
      author = 'Nick Barnes, David Jones',
      author_email = 'ccc-gistemp@climatecode.org',
      url = 'http://code.google.com/p/ccc-gistemp/',
      download_url =
      'http://ccc-gistemp.googlecode.com/files/ccc-gistemp-0.6.1.tar.gz',
      classifiers = filter(None, classifiers.split("\n")),
      platforms = 'windows',
      data_files = data_files,
      keywords = ['science', 'climate', 'GIS', 'temperature'],
     )
