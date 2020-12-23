#! /usr/bin/env python3

import subprocess
import http.server
from pathlib import Path
from threading import Thread
import os
import webbrowser
import signal

#Import time
import time

#This module defines a number of utilities for use by CGI scripts written in Python.
import cgi

#Establish Paths to Folders
import simImports

#Import the modules needed in this script
from orchestratorFile import OrchestratorFile
from kibanaManager import AWSKibanaHandler
from orchestrator import Orchestrator

#################################################################################
# SERVER INTERACTIONS HANDLING
#################################################################################

pathlist = []
class ServerHandler(http.server.BaseHTTPRequestHandler, Orchestrator, OrchestratorFile):
    '''
    This class will handle any incoming request from the browser 
    It derives from BaseHTTPRequestHandler
    '''

	#Handler for the GET requests
    def do_GET(self):

        if self.path.endswith("/WhatIfAnalysesTool/"):
            try:
                file = ("webGateway.html")
                mimetype = 'text/html'
                # Open the static file requested and send it
                with open(file) as f:
                    self.send_response(200)
                    self.send_header('Content-type', mimetype)
                    self.end_headers()
                    self.wfile.write(bytes(f.read(), "utf-8"))
                return
            except IOError:
                self.send_error(404,'This File Was Not Found: %s' % self.path)

        elif self.path.endswith('/WhatIfAnalysesTool/scenarioBundle'):

            mimetype = 'application/json'
            # Open the static file requested and send it
            with open(pathlist[-1]) as f:
                self.send_response(200)
                self.send_header('Content-type', mimetype)
                self.end_headers()
                self.wfile.write(bytes(f.read(), "utf-8"))
            return



    #Handler for the POST requests
    def do_POST(self):

        if self.path=="/send":
            form = cgi.FieldStorage(fp=self.rfile, 
                                    headers=self.headers,
                                    environ={'REQUEST_METHOD': 'POST',
                                    'CONTENT_TYPE': (self.headers['Content-Type']),})
            
            self.send_response(200)
            self.end_headers()

            #Get base path
            baseDirPath = self.getBasePath()

            runOrchestratorPath = '../../mcop-simulation-federates/sim_orchestrator/src/'

            #UI input
            self.scenarioFile              = baseDirPath + form["scenarioFile"].value
            modemModulationFile            = baseDirPath + form["modemModulationFile"].value
            outputFolder                   = baseDirPath + form["outputFolder"].value
            periodicUpdate                 = form["periodicUpdate"].value
            HOOPscenarioFile               = baseDirPath + form["HOOPscenarioFile"].value
            HOOPscenarioCompatibleFileName = form["HOOPscenarioCompatibleFileName"].value
            indexESName                    = form["indexName"].value

            #Script Input
            simulationClassList = "['pcdu','solararr','batt','payload','storageunit','receiver','transmitter','transceiver']"
            elevationAngleStep  = '0.01' #[deg]
            restoreFlag         = 'False'
            printOutput         = 'True'
            runningWhatIf       = 'True'
            indexConfigFile     = baseDirPath + 'mcop-simulation-whatif/input/index_hoopsim.json'
            simulatorName  = "whatIf"
            federationName = f"HOOPSIM_{simulatorName}"

            #Run the simulation with the defined arguments
            if "runSimulation" in form.keys():

                rs = Thread(target=subprocess.run, args=(['python', 
                                    runOrchestratorPath + 'orchestrator.py',
                                  '--scenarioFile',        self.scenarioFile,
                                  '--modemModulationFile', modemModulationFile,
                                  '--outputFolder',        outputFolder,
                                  '--periodicUpdate',      periodicUpdate,
                                  '--elevationAngleStep',  elevationAngleStep,
                                  '--fedName',             federationName,
                                  '--name',                simulatorName,
                                  '--simulationClassList', simulationClassList,
                                  '--runningWhatIf',       runningWhatIf,
                                  '--indexESName',         indexESName,
                                  '--indexConfigFile',     indexConfigFile,
                                # '--restoreFlag',         restoreFlag,
                                # '--printOutput',         printOutput
                                    ],))
                rs.start()


            #Call EXPORT function to transform scenario-bundle from HOOP in
            #WhatIf compatible format
            elif "exportHoopScenarioFile" in form.keys():
                #Use function from OrchestratorFile
                self.exportSimulationScenarioBundle(HOOPscenarioFile, outputFolder, HOOPscenarioCompatibleFileName)

            
            #Open simulation-scenario-bundle in a new tab
            elif "openScenarioFile" in form.keys():
                
                pathlist.append(self.scenarioFile)
                openScenarioURL = 'http://127.0.0.1:8080/WhatIfAnalysesTool/scenarioBundle'

                #open with firefox
                print("We recommend installing Mozilla Firefox for a better user experience.")

                #it will open a raw view of data in a second tab
                os.system(f'xdg-open {openScenarioURL}')

                
            elif "kibanaOutput" in form.keys():

                #################################
                #Open KIBANA Elasticsearch output
                #################################

                #Open kibana
                openIndexURL = 'https://search-hoopsim-xebvo4edd36kgunyxhaxct2tqi.eu-central-1.es.amazonaws.com/_plugin/kibana/app/management/kibana/indexPatterns'
                openDiscoverURL = 'https://search-hoopsim-xebvo4edd36kgunyxhaxct2tqi.eu-central-1.es.amazonaws.com/_plugin/kibana/app/discover#/'

                # open with firefox
                print("We recommend installing Mozilla Firefox for a better user experience.")
                os.system(f'xdg-open {openDiscoverURL}')

            elif "quit" in form.keys():
                os.kill(0, signal.SIGTERM)

            else:
                self.assassin.start()

            return

    def getBasePath(self):
        '''getBasePath
            Get base Path of the repositories in your local device
        '''

        currentPath = os.getcwd()
        cpList = currentPath.split('/')
        cpList.pop(-1)
        cpList.pop(-1)
        basePath = '/'.join(cpList)
        basePath = basePath + '/'

        return basePath

