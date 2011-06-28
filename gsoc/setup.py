#!/usr/bin/env python
# $URL$
# $Rev$
#
# setup.py
#
# Filipe Fernandes, 2011-05-29

import sys
from distutils.core import setup
from distutils.command.sdist import sdist

try: # Python 3
  from distutils.command.build_py import build_py_2to3 as build_py
except ImportError: # Python 2
  from distutils.command.build_py import build_py

mainscript = 'CCCgistemp/tool/ccc-gistemp'
data_files = [('',['readme.txt', 'LICENSE.txt', 'release-notes.txt'])]

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

if sys.platform == 'darwin':
    import py2app
    extra_options = dict(
        app=[mainscript],
        options=dict(py2app=dict(argv_emulation=True)),
        )
elif sys.platform == 'win32':
    import py2exe
    extra_options = dict(
        console=[{"script": mainscript,
        "icon_resources": [(1, "ccf.ico")]}],
        options = {"py2exe": {
            "compressed":1,
            "optimize":2,
            "bundle_files":2,
            "dist_dir":'dist',
            "xref":False,
            "skip_archive":False,
            "ascii": False,
            "custom_boot_script":''
            }},
        )
else:
    extra_options = dict(
        scripts=[mainscript],
        )

setup(name = 'ccc-gistemp',
      version='0.6.1',
      packages=['CCCgistemp','CCCgistemp.code','CCCgistemp.tool'],
      license='LICENSE.txt',
      description="""ccc-gistemp is a reimplementation of GISTEMP in Python""",
      long_description=open('readme.txt').read(), # change to capitals
      author='Nick Barnes, David Jones',
      author_email='ccc-gistemp@climatecode.org',
      url='http://code.google.com/p/ccc-gistemp/',
      download_url='http://ccc-gistemp.googlecode.com/files/ccc-gistemp-0.6.1.tar.gz',
      classifiers=filter(None, classifiers.split("\n")),
      platforms='any',
      cmdclass={'build_py': build_py},
      keywords=['science', 'climate', 'GIS', 'temperature'],
      **extra_options
     )
