#!/usr/bin/env python
# $URL$
# $Rev$
#
# packaging.py
#
# Filipe Fernandes, 2011-07-08

# http://docs.python.org/release/2.4.4/lib/module-os.path.html
import os
# http://www.python.org/doc/2.4.4/lib/module-sys.html
import sys
# http://docs.python.org/release/2.4.4/lib/module-subprocess.html
import subprocess

def get_setup():
    """
    Return information if the App is being called from a linux package,
    frozen (py2exe or py2app), or from source.
    """
    if hasattr(sys, 'frozen'):
        if sys.frozen in ('windows_exe', 'console_exe'):
            return 'py2exe'
        elif sys.frozen in ('macosx_app'):
            return 'py2app'
    elif not sys.argv[0].endswith('.py'):  # TODO: test on linux
        return 'packaged'
    return 'source'


def get_platform():
    """Safe way to determine platform during setup.py."""
    if sys.platform.startswith('win'):
        return 'windows'
    elif sys.platform.startswith('darwin'):
        return 'mac'
    return 'linux'

# I'll need this to launch default application when opening a file
def default_prog(filein):
    """Open the given file with the default program associate to it."""
    if hasattr(os, 'startfile'):  # windows
        os.startfile(filein)
    else:
        if sys.platform.startswith('darwin'):  # mac
            command = 'open'
        else:  # linux
            command = 'xdg-open'

        subprocess.call([command, filein])