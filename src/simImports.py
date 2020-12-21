#! /usr/bin/env python3

from pathlib import Path
import sys
import os

###############################################################################
# ESTABLISH PATHS TO FOLDERS
###############################################################################

simulationPlatformPath = Path(__file__).parent.joinpath('../../mcop-simulation-platform').resolve(True)
federatesPath = Path(__file__).parent.joinpath('../../mcop-simulation-federates').resolve(True)
modelsPath = Path(__file__).parent.joinpath('../../mcop-simulation-models').resolve(True)

relativePath = [
    str(federatesPath.joinpath('sim_federate/rti_connections')),
    str(federatesPath.joinpath('sim_federate/src')),
    str(federatesPath.joinpath('sim_orbit/rti_connections')),
    str(federatesPath.joinpath('sim_orbit/src')),
    str(federatesPath.joinpath('sim_orchestrator/rti_connections')),
    str(federatesPath.joinpath('sim_orchestrator/src')),
    str(federatesPath.joinpath('sim_shared/src')),
    str(federatesPath.joinpath('util')),
    str(federatesPath.joinpath('libs')),

    str(modelsPath.joinpath('sim_batt/src')),
    str(modelsPath.joinpath('sim_payload/src')),
    str(modelsPath.joinpath('sim_pcdu/src')),
    str(modelsPath.joinpath('sim_receiver/src')),
    str(modelsPath.joinpath('sim_shared/src')),
    str(modelsPath.joinpath('sim_solararr/src')),
    str(modelsPath.joinpath('sim_storageunit/src')),
    str(modelsPath.joinpath('sim_transmitter/src')),
    str(modelsPath.joinpath('sim_transceiver/src')),
]
paths = ":".join(relativePath)
#Establish a python environment needed when executing functions in other repos
os.environ["PYTHONPATH"] = paths + ":" + ("" if os.environ.get("PYTHONPATH") == None else os.environ.get("PYTHONPATH"))

#As the paths established above are not immediate to take action, there 
# is need to establish there here in other way
# The folders beeing used here are used during the execution of functions in this repo
sys.path.insert(0, '../../mcop-simulation-federates/sim_orchestrator/src')
sys.path.insert(0, '../../mcop-simulation-federates/sim_orchestrator/rti_connections')
sys.path.insert(0, '../../mcop-simulation-federates/sim_shared/src')
sys.path.insert(0, '../../mcop-simulation-federates/util')
sys.path.insert(0, '../../mcop-simulation-models/sim_batt/src')
sys.path.insert(0, '../../mcop-simulation-models/sim_payload/src')
sys.path.insert(0, '../../mcop-simulation-models/sim_pcdu/src')
sys.path.insert(0, '../../mcop-simulation-models/sim_receiver/src')
sys.path.insert(0, '../../mcop-simulation-models/sim_shared/src')
sys.path.insert(0, '../../mcop-simulation-models/sim_solararr/src')
sys.path.insert(0, '../../mcop-simulation-models/sim_storageunit/src')
sys.path.insert(0, '../../mcop-simulation-models/sim_transmitter/src')
sys.path.insert(0, '../../mcop-simulation-models/sim_transceiver/src')
