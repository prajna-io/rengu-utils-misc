#!/usr/bin/env python

import sys
from os import environ, rename
from hashlib import sha256
from pathlib import Path

BUFFER_SIZE = 8192

bindir = environ["RENGU_BINDIR"]

for fname in sys.argv[1:]:

    old_path = Path(fname)
    bin_hash = sha256()

    with open(fname, "rb") as fd:
        for buf in iter(lambda: fd.read(BUFFER_SIZE), b""):
            bin_hash.update(buf)

    # Determine new bin address location
    bin_hex = str(bin_hash.hexdigest())
    bin_path = Path(bindir) / f"{bin_hex[0:2]}" / f"{bin_hex[2:4]}" / f"{bin_hex[4:]}"

    bin_path.parent.mkdir(parents=True, exist_ok=True)

    old_path.rename(bin_path)
