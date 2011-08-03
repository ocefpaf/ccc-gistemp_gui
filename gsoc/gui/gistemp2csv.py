#!/usr/bin/env python
# $URL$
# $Rev$
#
# gistemp2csv.py
#
# Filipe Fernandes, 2011-08-01

import os
import re
import csv

def gistemp2csv(fin):
    """
    Write a comma separated value file from ccc-gistemp text output.
    """

    basename = os.path.splitext(os.path.basename(fin))[0]

    fout = open(basename + '.csv', 'wb')

    csv_out = csv.writer(fout, delimiter=',')
    header = []
    field = ''

    with open(fin) as lines:
        for line in lines:
            if re.match(r"^(18|19|20)\d{2}", line):
                # Remove the last redundant year entry.
                data = line.strip().split()[:-1]
                # Write rows with years and temperatures anomalies
                csv_out.writerow(data)

                # TODO: Handle the asterisks.
                if len(data) != length:
                    print("Warning, this line has less entries than expected\n" + data)

            elif re.match(r"^Year", line) and (not field):
                # Write only first occurrence of the filed descriptor.
                field = line.split()[:-1]
                csv_out.writerow(field)
                length = len(field)

            elif line.strip() and (not field):
                header += line

    header = ''.join(header)
    fout.close()

    with open(basename + '.csv', "r+") as f:
        old = f.read()
        f.seek(0)
        f.write(header + '\n' + old)

if __name__ == '__main__':
    import glob
    files = glob.glob("*.txt")
    # TODO: The Zonnal files have a different field.
    #                            24N   24S   90S     64N   44N   24N   EQU   24S   44S   64S   90S
    # Year  Glob  NHem  SHem    -90N  -24N  -24S    -90N  -64N  -44N  -24N  -EQU  -24S  -44S  -64S
    # where 24N and -90N should be placed in the same cell (I guess!?).
    for f in files:
        gistemp2csv(f)
