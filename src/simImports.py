#! /usr/bin/env python3

##############################################################################
####                         IMPORT WORKING FOLDER                      ######
##############################################################################

import os
from pathlib import Path

simulationPlatformPath = Path(__file__).parent.joinpath('../../mcop-simulation-platform').resolve(True)
federatesPath          = Path(__file__).parent.joinpath('../../mcop-simulation-federates').resolve(True)
modelsPath             = Path(__file__).parent.joinpath('../../mcop-simulation-models').resolve(True)

def initializeSysPath():
    relativePath = [
        str(federatesPath.joinpath('sim_federate/rti_connections')),
        str(federatesPath.joinpath('sim_federate/src')),
        str(federatesPath.joinpath('sim_orbit/rti_connections')),
        str(federatesPath.joinpath('sim_orbit/src')),
        str(federatesPath.joinpath('sim_orchestrator/rti_connections')),
        str(federatesPath.joinpath('sim_orchestrator/AWSKibana')),
        str(federatesPath.joinpath('sim_orchestrator/src')),
        str(federatesPath.joinpath('sim_shared/src')),
        str(federatesPath.joinpath('util')),
        str(federatesPath.joinpath('libs')),

        str(modelsPath.joinpath('sim_batt/src')),
        str(modelsPath.joinpath('sim_battKibam/src')),
        str(modelsPath.joinpath('sim_payload/src')),
        str(modelsPath.joinpath('sim_pcdu/src')),
        str(modelsPath.joinpath('sim_receiver/src')),
        str(modelsPath.joinpath('sim_shared/src')),
        str(modelsPath.joinpath('sim_solararr/src')),
        str(modelsPath.joinpath('sim_storageunit/src')),
        str(modelsPath.joinpath('sim_thermal/src')),
        str(modelsPath.joinpath('sim_transmitter/src')),
        str(modelsPath.joinpath('sim_transceiver/src')),
    ]
    paths = ":".join(relativePath)
    os.environ["PYTHONPATH"] = paths + ":" + ("" if os.environ.get("PYTHONPATH") == None else os.environ.get("PYTHONPATH"))

initializeSysPath()

# -*- coding: utf-8 -*-