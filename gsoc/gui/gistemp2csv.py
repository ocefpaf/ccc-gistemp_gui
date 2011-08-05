#!/usr/bin/env python
# $URL$
# $Rev$
#
# gistemp2csv.py
#
# Filipe Fernandes, 2011-08-01

# http://docs.python.org/release/2.4.4/lib/module-os.path.html
import os
# http://docs.python.org/release/2.4.4/lib/module-re.html
import re
# http://docs.python.org/release/2.4.4/lib/module-csv.html
import csv


def chunks(l, n):
    """
    return n-sized chunks from  the list l.
    """
    return [l[i:i + n] for i in range(0, len(l), n)]


def non_zonal(line):
    """Break Non-Zonal file format into specified chunks."""

    # The first 12 entries are 5 characters width columns.
    month = chunks(line[:65], 5)
    # After 3 white spaces it becomes 4 characters width columns.
    year = chunks(line[68:76], 4)
    # After 2 white spaces it is back to 5 characters width columns.
    # the -5 removes the last redundant year entry.
    season = chunks(line[78:-5], 5)
    # Write rows with years and temperatures anomalies.
    return month + year + season


def gistemp2csv(fin):
    """ Write a comma separated value file from ccc-gistemp text output."""

    basename = os.path.splitext(os.path.basename(fin))[0]

    fout = open(basename + '.csv', 'wb')

    csv_out = csv.writer(fout, delimiter=',')

    header = []
    field1 = ''
    field2 = ''

    with open(fin) as lines:
        for line in lines:
            # If start with with a number Year it is data.
            if re.match(r"^(18|19|20)\d{2}", line):
                # Non-Zonal avg files are treated differently.
                if not 'Zon' in basename:
                    data = non_zonal(line)
                else:
                    data = line.split()[:-1]
                csv_out.writerow(data)

            # Write only first occurrence of the field descriptor 1.
            elif re.match(r"^Year", line) and (not field1):
                field1 = line.split()[:-1]
                csv_out.writerow(field1)

            # Write only first occurrence of the field descriptor 2.
            # only Zonal avg files have this second descriptor.
            elif "90S" in line and (not field2):
                field2 = [' '] * 5 + line.split()[:-1]
                csv_out.writerow(field2)

            # This passes fields 1 and 2 and blank lines.
            # Keeping all the rest as header.
            elif line.strip() and (not field1) and (not field2):
                header += line

    header = ''.join(header)
    fout.close()

    # Write the header without the commas.
    with open(basename + '.csv', "r+") as f:
        old = f.read()
        f.seek(0)
        f.write(header + '\n' + old)


if __name__ == '__main__':
    import glob
    files = glob.glob("*.txt")
    for f in files:
        gistemp2csv(f)
