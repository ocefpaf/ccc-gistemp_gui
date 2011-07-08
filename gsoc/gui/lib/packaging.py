#!/usr/bin/env python
# $URL$
# $Rev$
#
# packaging.py
#
# Filipe Fernandes, 2011-07-08

# http://www.python.org/doc/2.4.4/lib/module-sys.html
import sys
# http://docs.python.org/release/2.4.4/lib/module-os.path.html
import os

def get_setup():
    """
    Return information if the App is being called from a linux package,
    frozen (py2exe or py2app), or from source.
    """
    if hasattr(sys, 'frozen'):
        frozen = getattr(sys, 'frozen', '')
        return frozen
    elif is_packaged(): # linux
        return 'packaged'
    return 'source'

def is_packaged():
    """Return True if the App is packaged (linux only)."""
    return not sys.argv[0].endswith('.py')

def get_platform():
    """safer way to determine platform. """
    if sys.platform.startswith('win'):
        return 'windows'
    elif sys.platform.startswith('darwin'):
        return 'mac'
    return 'linux'

# I'll need this to launch default application when opening a file
#if hasattr(os, 'startfile'):# windows
    #os.startfile(path)
#else:
    #if sys.platform.startwith('darwin'): # mac
        #command = 'open'
    #else: # linux
        #command = 'xdg-open'
    #subprocess.call([command, path])