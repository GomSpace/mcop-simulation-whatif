#! /usr/bin/env python3

##############################################################################
####                       IMPORT WORKING FOLDERS                       ######
##############################################################################

import sys
from pathlib import Path

federatesPath = Path(__file__).parent.joinpath('../../mcop-simulation-federates').resolve(True)

sys.path.insert(0, str(federatesPath))

import importProject

# -*- coding: utf-8 -*-