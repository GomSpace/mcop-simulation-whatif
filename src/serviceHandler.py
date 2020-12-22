#! /usr/bin/env python3

import subprocess
import http.server
from threading import Thread
import os
import signal

#This module defines a number of utilities for use by CGI scripts written in Python.
import cgi

#Establish Paths to Folders
import simImports

#Import the modules needed in this script
from orchestratorFile import OrchestratorFile

#################################################################################
# SERVER INTERACTIONS HANDLING
#################################################################################


class ServerHandler(http.server.BaseHTTPRequestHandler, OrchestratorFile):
    """
    This class will handle any incoming request from the browser 
    It derives from BaseHTTPRequestHandler
    """

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
            if self.path.endswith(".json"):
                mimetype = 'application/json'
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

        if self.path=="/send":
            form = cgi.FieldStorage(fp=self.rfile, 
                                    headers=self.headers,
                                    environ={'REQUEST_METHOD': 'POST',
                                    'CONTENT_TYPE': (self.headers['Content-Type']),})
            
            self.send_response(200)
            self.end_headers()

            #Get base path
            basePath = self.getBasePath()

            runOrchestratorPath = '../../mcop-simulation-federates/sim_orchestrator/src/'

            #UI input
            scenarioFile                   = basePath + form["scenarioFile"].value
            modemModulationFile            = basePath + form["modemModulationFile"].value
            outputFolder                   = basePath + form["outputFolder"].value
            periodicUpdate                 = form["periodicUpdate"].value
            HOOPscenarioFile               = basePath + form["HOOPscenarioFile"].value
            HOOPscenarioCompatibleFileName = form["HOOPscenarioCompatibleFileName"].value
            indexESName                    = form["indexName"].value

            #Script Input
            simulationClassList = "['pcdu','solararr','batt','payload','storageunit','receiver','transmitter','transceiver']"
            elevationAngleStep  = '0.01' #[deg]
            restoreFlag         = 'False'
            printOutput         = 'True'
            runningWhatIf       = 'True'
            indexConfigFile     = basePath + 'mcop-simulation-whatif/input/index_hoopsim.json'
            simulatorName = "whatIf"
            federationName = f"HOOPSIM_{simulatorName}"

            #Run the simulation with the defined arguments
            if "runSimulation" in form.keys():

                rs = Thread(target=subprocess.run, args=(['python3', 
                                    runOrchestratorPath + 'orchestrator.py',
                                  '--scenarioFile',        scenarioFile,
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
                #get file from base
                try:
                    #open in a default desktop program
                    os.system(f'xdg-open ../../{form["scenarioFile"].value}')
                except:
                    try:
                        #open in the command line
                        os.system(f'cat ../../{form["scenarioFile"].value}')
                    except:
                        #if on windows, open in a default desktop program
                        os.system(scenarioFile)

                
            elif "kibanaOutput" in form.keys():

                #################################
                #Open KIBANA Elasticsearch output
                #################################

                #Open kibana
                openIndex = 'https://search-hoopsim-xebvo4edd36kgunyxhaxct2tqi.eu-central-1.es.amazonaws.com/_plugin/kibana/app/management/kibana/indexPatterns'
                openDiscover = 'https://search-hoopsim-xebvo4edd36kgunyxhaxct2tqi.eu-central-1.es.amazonaws.com/_plugin/kibana/app/discover#/'

                os.system(f'xdg-open {openDiscover}')

            elif "quit" in form.keys():
                os.kill(0, signal.SIGTERM)

            else:
                self.assassin.start()

            return

    def getBasePath(self):
        """getBasePath
            Get base Path of the repositories in your local device
        """

        currentPath = os.getcwd()
        cpList = currentPath.split('/')
        cpList.pop(-1)
        cpList.pop(-1)
        basePath = '/'.join(cpList)
        basePath = basePath + '/'

        return basePath
