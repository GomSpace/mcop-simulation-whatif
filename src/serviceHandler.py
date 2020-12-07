#! /usr/bin/env python3

import subprocess
import http.server
from pathlib import Path
import sys

#This module defines a number of utilities for use by CGI scripts written in Python.
import cgi
from os import curdir, sep, chdir, getcwd

import os


################################################################################
#Import working folders
import os

from threading import Thread
import subprocess
import gc

import webbrowser

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
os.environ["PYTHONPATH"] = paths + ":" + ("" if os.environ.get("PYTHONPATH") == None else os.environ.get("PYTHONPATH"))

#Import ORCHESTRATOR file managment
#(the paths established above are not immediate to take action)
sys.path.insert(0, '../../mcop-simulation-federates/sim_orchestrator/src')
sys.path.insert(0, '../../mcop-simulation-federates/sim_shared/src')
sys.path.insert(0, '../../mcop-simulation-models/sim_batt/src')
sys.path.insert(0, '../../mcop-simulation-models/sim_payload/src')
sys.path.insert(0, '../../mcop-simulation-models/sim_pcdu/src')
sys.path.insert(0, '../../mcop-simulation-models/sim_receiver/src')
sys.path.insert(0, '../../mcop-simulation-models/sim_shared/src')
sys.path.insert(0, '../../mcop-simulation-models/sim_solararr/src')
sys.path.insert(0, '../../mcop-simulation-models/sim_storageunit/src')
sys.path.insert(0, '../../mcop-simulation-models/sim_transmitter/src')
sys.path.insert(0, '../../mcop-simulation-models/sim_transceiver/src')
from orchestratorFile import OrchestratorFile


#################################################################################
# SERVER INTERACTIONS HANDLING
#################################################################################

class ServerHandler(http.server.BaseHTTPRequestHandler, OrchestratorFile): #OrchestratorFile
    '''
    This class will handle any incoming request from the browser 
    It derives from BaseHTTPRequestHandler
    '''
	#Handler for the GET requests
    def do_GET(self):
        self.path = ("webGateway.html")
        
        try:
            #Check the file extension required and
    		#set the right mime type
            sendReply = False
            if self.path.endswith(".html"):
                mimetype = 'text/html'
                sendReply = True
            if self.path.endswith(".jpg"):
                mimetype = 'image/jpg'
                sendReply = True
            if self.path.endswith(".gif"):
                mimetype = 'image/gif'
                sendReply = True
            if self.path.endswith(".js"):
                mimetype = 'application/javascript'
                sendReply = True
            if self.path.endswith(".css"):
                mimetype = 'text/css'
                sendReply = True

            if sendReply == True:
                # Open the static file requested and send it
                with open(self.path) as f:
                    self.send_response(200)
                    self.send_header('Content-type', mimetype)
                    self.end_headers()
                    self.wfile.write(bytes(f.read(), "utf-8"))
                return
        except IOError:
            self.send_error(404,'This File Was Not Found: %s' % self.path)
            
    #Handler for the POST requests
    def do_POST(self):
        print('entered do_POST')
        if self.path=="/send":
            form = cgi.FieldStorage(fp=self.rfile, 
                                    headers=self.headers,
                                    environ={'REQUEST_METHOD': 'POST',
                                    'CONTENT_TYPE': (self.headers['Content-Type']),})
            
            self.send_response(200)
            self.end_headers()


            runOrchestratorPath = '../../mcop-simulation-federates/sim_orchestrator/src/'

            #Read form the main window the value
            scenarioFile        = form["scenarioFile"].value
            modemModulationFile = form["modemModulationFile"].value
            outputFolder        = form["outputFolder"].value
            periodicUpdate      = form["periodicUpdate"].value
            HOOPscenarioFile    = form["HOOPscenarioFile"].value
            HOOPscenarioCompatibleFileName = form["HOOPscenarioCompatibleFileName"].value
            simulationClassList = "['pcdu','solararr','batt','payload','storageunit','receiver','transmitter','transceiver']"
            elevationAngleStep  = '0.01' #[deg]
            restoreFlag         = 'False'
            printOutput         = 'True'

            simulatorName = "whatIf"
            federationName = "HOOPSIM_{}".format(simulatorName)

            #Run the simulation with the defined arguments
            if "runSimulation" in form.keys():

                rs = Thread(target=subprocess.run, args=(['python', 
                                    runOrchestratorPath + 'orchestrator.py',
                                  '--scenarioFile',        scenarioFile,
                                  '--modemModulationFile', modemModulationFile,
                                  '--outputFolder',        outputFolder,
                                  '--periodicUpdate',      periodicUpdate,
                                  '--elevationAngleStep',  elevationAngleStep,
                                  '--fedName',             federationName,
                                  '--name',                simulatorName,
                                  '--simulationClassList', simulationClassList
                                #   '--restoreFlag',         restoreFlag,
                                #   '--printOutput',         printOutput
                                                            ],))
                rs.start()


            #Call EXPORT function to transform scenario-bundle from HOOP in
            #WhatIf compatible format
            elif "exportHoopScenarioFile" in form.keys():
                #Use function from OrchestratorFile
                #(inputScenarioFile,outputScenarioFolder)
                self.exportSimulationScenarioBundle(HOOPscenarioFile, outputFolder, HOOPscenarioCompatibleFileName)

            
            #Open simulation-scenario-bundle in a new tab
            elif "openScenarioFile" in form.keys():
                # filename = '/mnt/c/users/maan/projects/mcop-simulation-federates/input/simulation-scenario-bundle.json'
                # webbrowser.open('file://' + os.path.realpath(filename))
                pass
                
                
                
            #Call the output in KIBANA
            elif "kibanaOutput" in form.keys():
                pass
            # util.generatorRandomScenario

            else:
                self.assassin.start()

            return



# #! /usr/bin/env python3

# import sys, os
# import shutil
# import argparse
# import logging
# import logging.config
# import http.server
# import threading
# import subprocess

# import runWhatIf

# APP_NAME = 'mcop-sim-platform-gateway'
# APP_VERSION = '0.1'
# PORT_NUMBER = 8080
# MY_FOLDER = os.path.dirname(os.path.realpath(__file__))

# logging.basicConfig(stream = sys.stdout, level = logging.DEBUG,             
#                     format = '%(levelname)-8s [%(name)-8s] %(message)s',)

# def parse_args():
#     """ Parsing arguments """

#     def host_port(s):
#         """ host:port type for argparse"""
#         try:
#             host, port = s.split(':')
#             port = int(port)
#             return host, port
#         except:
#             raise argparse.ArgumentTypeError('Server hostname must be address:port')

#     parser = argparse.ArgumentParser(description = 'To parse some simple arguments',
#                                      formatter_class = argparse.ArgumentDefaultsHelpFormatter)
#     parser.add_argument('-iM', '--inputMode',
#                         nargs='+',
#                         type=str,
#                         default='webserver',
#                         help='Input mode launching the simulation platform (''webserver'' launches a webserver that wait for a form to be input; ''direct'' directly processes the command line arguments to launch the supervisor', metavar = 'webserver or direct')
#     parser.add_argument('-ha', '--http-listen-address',
#                         type=str,
#                         default='127.0.0.1',
#                         help='Embedded webserver listen address', metavar='127.0.0.1 or ::')
#     parser.add_argument('-hp', '--http-listen-port',
#                         type=int,
#                         default=8080,
#                         help='Embedded webserver listen port', metavar='8080')
#     parser.add_argument('-hP', '--http-admin-passwd',
#                         type=str,
#                         default='admin',
#                         help='Embedded webserver admin password (for write routes)', metavar='admin')
#     parser.add_argument('-d', '--debug',
#                         action='store_true',
#                         help='Set default logger level to DEBUG instead of INFO')
	
#     return parser.parse_args() 

# def main(args):
#     """
#     Starting application...
#     """
#     if args.inputMode == 'webserver':
#         print('Webserver is being launched')
#         try:
#             #Create a web server and define the handler to manage the
#             #incoming request
#             server_handler = runWhatIf.ServerHandler
#             server_handler.args = args
#             server = http.server.HTTPServer(('', PORT_NUMBER), server_handler)
#             print('Started httpserver on port ', PORT_NUMBER)	
            
#             # Pipe a new thread on the socket.close method in order to close the server
#             # from the do_post command. Not sure if
#             # server.socket.close is more appropriate than server.shutdown
#             server_handler.assassin = threading.Thread(target=server.shutdown)
#             server_handler.assassin.daemon = True
            
#             #Wait forever for incoming http requests
#             server.serve_forever()
#         # This part of code below is apparently not necessary to catch the ctrl+c
#         except KeyboardInterrupt:
#             print('^C received, shutting down the web server')
#             server.socket.close()
#     else:
#         print('Not implemented yet')
    
#     # Coded but useless as tsh is no event programming yet
#     logger.info("Event loop running forever, press Ctrl+C to interrupt.")
#     logger.info("pid %s: send SIGINT or SIGTERM to exit." % os.getpid())
     
# if __name__ == '__main__':
#     # Raise terminal size to maximum
#     os.environ['COLUMNS'] = str(shutil.get_terminal_size().columns)

#     # Init logger
#     logging.basicConfig(level=logging.DEBUG, format = '%(levelname)-8s [%(name)-8s] %(message)s')
   
#     logger = logging.getLogger('__main__')
    
#     # Parse arguments for basic configuration of the federate
#     print("Parsing command line arguments")
#     args = parse_args()
    
#     main(args)

# # -*- coding: utf-8 -*-


'''
            federationName = "HOOPSIM_{}".format(naodulationFile', modemModulationFile,
                                  '--outputFolder',        outputFolder,
                                  '--periodicUpdate',      periodicUpdate,
                                  '--name',                simulatorName,
                                  '--elevationAngleStep',  elevationAngleStep,
                                  '--fedName',             fedName,
                                  '--simulationClassList', simulationClassList)
'''


# sys.path.insert(0, '../../mcop-simulation-federates/sim_orchestrator/src')
# sys.path.insert(0, '../../mcop-simulation-platform/src')
# sys.path.insert(0, '../../mcop-simulation-federates/util')

# sys.path.insert(0, '../../mcop-simulation-platform')
# sys.path.insert(0, '../../mcop-simulation-federates')
# sys.path.insert(0, '../../mcop-simulation-models')

# sys.path.insert(0, '../../mcop-simulation-federates/sim_federate/rti_connections')
# sys.path.insert(0, '../../mcop-simulation-federates/sim_federate/src')
# sys.path.insert(0, '../../mcop-simulation-federates/sim_orbit/rti_connections')
# sys.path.insert(0, '../../mcop-simulation-federates/sim_orbit/src')
# sys.path.insert(0, '../../mcop-simulation-federates/sim_orchestrator/rti_connections')
# sys.path.insert(0, '../../mcop-simulation-federates/sim_orchestrator/src')
# sys.path.insert(0, '../../mcop-simulation-federates/sim_shared/src')
# sys.path.insert(0, '../../mcop-simulation-federates/util')
# sys.path.insert(0, '../../mcop-simulation-federates/libs')

# sys.path.insert(0, '../../mcop-simulation-models/sim_batt/src')
# sys.path.insert(0, '../../mcop-simulation-models/sim_payload/src')
# sys.path.insert(0, '../../mcop-simulation-models/sim_pcdu/src')
# sys.path.insert(0, '../../mcop-simulation-models/sim_receiver/src')
# sys.path.insert(0, '../../mcop-simulation-models/sim_shared/src')
# sys.path.insert(0, '../../mcop-simulation-models/sim_solararr/src')
# sys.path.insert(0, '../../mcop-simulation-models/sim_storageunit/src')
# sys.path.insert(0, '../../mcop-simulation-models/sim_transmitter/src')
# sys.path.insert(0, '../../mcop-simulation-models/sim_transceiver/src')

'''
import pathlib

uri = pathlib.Path("/mnt/c/users/maan/projects/mcop-simulation-federates/input/simulation-scenario-bundle.json").as_uri()
print('uri', uri)

pathname = "/mnt/c/users/maan/projects/mcop-simulation-federates/input/simulation-scenario-bundle.json" 

from urllib.parse import urljoin
from urllib.request import pathname2url

print(urljoin('file:', pathname2url(pathname)))

import requests
r = requests.get('url')
print (r.json())

'''