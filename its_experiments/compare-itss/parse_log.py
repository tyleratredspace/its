#!/usr/bin/env python3
import csv
import re
import sys

with open(sys.argv[1]) as f:
    lines = f.readlines()

with open('output.csv', 'w') as ofile:
    out = csv.DictWriter(ofile, ('maybe_time', 'status', 'bytes', 'url'))
    out.writeheader()

    for line in lines:
        group = re.match('^[\d\-:TZ\.]+ [\w\-]+ [\d\.:]+ [\d\.:]+ [\d\.]+ (?P<maybe_time>[\d\.]+) [\d\.]+ \d+ (?P<status>\d+) \d+ (?P<bytes>\d+) "GET (?P<url>.+?) HTTP/\d\.\d"', line).groupdict()
        out.writerow(group)