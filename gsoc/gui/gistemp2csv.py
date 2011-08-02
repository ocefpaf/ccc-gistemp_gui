#!/usr/bin/env python
# $URL$
# $Rev$
#
# gistemp2csv.py
#
# Filipe Fernandes, 2011-08-01

import csv
import re

def gistemp2csv(fin="mixedGLB.Ts.ho2.GHCN.CL.PA.txt",
                fout="mixedGLB.Ts.ho2.GHCN.CL.PA.csv"):
    """
    """
    csv_out = csv.writer(open(fout, 'wb'), delimiter=',')
    header = []

    with open(fin) as lines:
        for line in lines:
            if re.match("^[1-9]+.*", line):
                csv_out.writerow(line.strip().split())
            elif re.match("^Year+.*", line):
                csv_out.writerow(line.strip().split())
            else:
                if line.strip():
                    header += line

    with open(fout, "r+") as f:
        old = f.read()
        f.seek(0)
        f.write(''.join(header) + '\n' + old)

if __name__ == '__main__':
    gistemp2csv()