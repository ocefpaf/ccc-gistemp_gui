#!/usr/bin/env python
# $URL$
# $Rev$
#
# ccc-gistemp.py
#
# Filipe Fernandes, 2011-06-05

"""Tool that takes python script and runs it."""

import sys
from main import main
from options import parse_options, option_parser

def commandline_call():
    """Entry point of the program when called from the command line."""
    options, args = parse_options(sys.argv[1:])
    
    if not len(args)==1:
        if len(args)==0:
            option_parser.print_help()
        else:
            print  >> sys.stderr, "1 argument: input file"
        sys.exit(1)

    import time
    t1 = time.time()
    if args[0] == "-":
        pyfile = sys.stdin
    else:
        pyfile = open(args[0],"r")

    # store the name of the input file for later use
    options.update({'infilename':args[0]})

    main(pyfile, overrides=options)
    # FIXME: what about the options defined in the script: options.quiet
    if not 'quiet' in options:
        print >>sys.stderr, "Ran script in %.2fs" % (time.time() - t1)


if __name__ == '__main__':
    commandline_call()
