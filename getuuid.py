#!/usr/bin/env python

import sys
import re
import warnings

UUID = re.compile("[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}")

page = sys.stdin.read()

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    for match in UUID.finditer(page):
        print(match[0])
