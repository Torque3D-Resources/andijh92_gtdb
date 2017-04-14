# Execute this file with python on Windows to start GTDB!
# It looks like: right click -> open with -> python

import sys
import os

sys.path.append(os.path.abspath("."))

configPyContent = """
import os
VERSION = '0.1'
DATADIR = os.path.abspath('./data') """

with open("gtdb/Config.py", "w") as f:
    f.write(configPyContent)

execfile('gtdb/gtdb')
