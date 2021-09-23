#!/usr/bin/env python3.8
from configparser import ConfigParser, ExtendedInterpolation
import sys
import time

###############################################################################
from astropy.io import fits
import numpy as np

###############################################################################
parser = ConfigParser(interpolation=ExtendedInterpolation())
parser.read('meta.ini')
############################################################
# to import from src since I'm in a difrent leaf of a the tree structure
# work_directory = parser.get("directories", "work")
# sys.path.insert(0, f"{work_directory}")
################################################################################
###############################################################################
ti = time.time()
###############################################################################
dap_location = parser.get('files', 'dap')
dap_all = fits.open(dap_location)
###############################################################################
tf = time.time()
print(f"Running time: {tf-ti:.2f}")
