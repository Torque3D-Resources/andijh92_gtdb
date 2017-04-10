"""
Some informations from './configure', 'make' and 'make install'.
"""

import sys
import os

VERSION = '0.1'
TESTSDIR = os.path.abspath('./tests')
DATADIR = os.path.abspath('./data') if '${prefix}' in '${prefix}/share' else '${prefix}/share'
