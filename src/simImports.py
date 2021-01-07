#! /usr/bin/env python3

##############################################################################
####                         IMPORT WORKING FOLDER                      ######
##############################################################################


from pathlib import Path

federatesPath          = Path(__file__).parent.joinpath('../../mcop-simulation-federates').resolve(True)
modelsPath             = Path(__file__).parent.joinpath('../../mcop-simulation-models').resolve(True)

import os
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

import sys
sys.path.insert(0, str(federatesPath.joinpath('sim_federate/rti_connections')))
sys.path.insert(0, str(federatesPath.joinpath('sim_federate/rti_connections')))
sys.path.insert(0, str(federatesPath.joinpath('sim_federate/src')))
sys.path.insert(0, str(federatesPath.joinpath('sim_orbit/rti_connections')))
sys.path.insert(0, str(federatesPath.joinpath('sim_orbit/src')))
sys.path.insert(0, str(federatesPath.joinpath('sim_orchestrator/rti_connections')))
sys.path.insert(0, str(federatesPath.joinpath('sim_orchestrator/AWSKibana')))
sys.path.insert(0, str(federatesPath.joinpath('sim_orchestrator/src')))
sys.path.insert(0, str(federatesPath.joinpath('sim_shared/src')))
sys.path.insert(0, str(federatesPath.joinpath('util')))
sys.path.insert(0, str(federatesPath.joinpath('libs')))

sys.path.insert(0, str(modelsPath.joinpath('sim_batt/src')))
sys.path.insert(0, str(modelsPath.joinpath('sim_battKibam/src')))
sys.path.insert(0, str(modelsPath.joinpath('sim_payload/src')))
sys.path.insert(0, str(modelsPath.joinpath('sim_pcdu/src')))
sys.path.insert(0, str(modelsPath.joinpath('sim_receiver/src')))
sys.path.insert(0, str(modelsPath.joinpath('sim_shared/src')))
sys.path.insert(0, str(modelsPath.joinpath('sim_solararr/src')))
sys.path.insert(0, str(modelsPath.joinpath('sim_storageunit/src')))
sys.path.insert(0, str(modelsPath.joinpath('sim_thermal/src')))
sys.path.insert(0, str(modelsPath.joinpath('sim_transmitter/src')))
sys.path.insert(0, str(modelsPath.joinpath('sim_transceiver/src')))


# -*- coding: utf-8 -*-