#! /usr/bin/env python3

import subprocess
import http.server
from threading import Thread
import os
import signal

#This module defines a number of utilities for use by CGI scripts written in Python.
import cgi

#Import project folders
import simImports

#Import the modules needed in this script
from logger           import Logger
from orchestratorFile import OrchestratorFile

#################################################################################
# SERVER INTERACTIONS HANDLING
#################################################################################

class ServerHandler(http.server.BaseHTTPRequestHandler, OrchestratorFile, Logger):
    """
    This class will handle any incoming request from the browser 
    It derives from BaseHTTPRequestHandler
    """

    pathList : list = []

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
            #Restore ABORT
            self.ABORT = False
            
            form = cgi.FieldStorage(fp=self.rfile, 
                                    headers=self.headers,
                                    environ={'REQUEST_METHOD': 'POST',
                                    'CONTENT_TYPE': (self.headers['Content-Type']),})
            
            self.send_response(200)
            self.end_headers()
            #Get root Directory path
            rootDirPath = self.getBasePath()

            runOrchestratorPath = '../../mcop-simulation-federates/sim_orchestrator/src/'

            #UI input
            scenarioFile                   = os.path.join(rootDirPath,form["scenarioFile"].value)
            modemModulationFile            = os.path.join(rootDirPath, form["modemModulationFile"].value)
            outputFolder                   = os.path.join(rootDirPath, form["outputFolder"].value)
            periodicUpdate                 = form["periodicUpdate"].value
            HOOPscenarioFile               = os.path.join(rootDirPath, form["HOOPscenarioFile"].value)
            HOOPscenarioCompatibleFileName = form["HOOPscenarioCompatibleFileName"].value
            indexESName                    = form["indexName"].value

            #Script Input
            elevationAngleStep  = '0.01' #[deg]
            runningWhatIf       = 'True'
            indexConfigFile     = os.path.join(rootDirPath, 'mcop-simulation-federates/sim_orchestrator/AWSKibana/indexHOOPSIM.json')
            simulatorName       = "standalone"
            federationName      = f"HOOPSIM_{simulatorName}"
            
            #Run the simulation with the defined arguments
            if "runSimulation" in form.keys():
                
                #Get check button if run thermal model or not
                try:
                    runningThermal  = True if form["thermal"].value == 'on' else False
                except:
                    runningThermal  = False
                
                rs = Thread(target=subprocess.run, args=(['python3', 
                                    runOrchestratorPath + 'orchestrator.py',
                                  '--scenarioFile',        scenarioFile,
                                  '--modemModulationFile', modemModulationFile,
                                  '--outputFolder',        outputFolder,
                                  '--periodicUpdate',      periodicUpdate,
                                  '--elevationAngleStep',  elevationAngleStep,
                                  '--fedName',             federationName,
                                  '--name',                simulatorName,
                                  '--runningWhatIf',       runningWhatIf,
                                  '--runningThermal',      str(runningThermal),
                                  '--indexESName',         indexESName,
                                  '--indexConfigFile',     indexConfigFile,
                                    ],))
                rs.start()

            #Open simulation-scenario-bundle in a new tab
            elif "openScenarioFile" in form.keys():
                #get file from base
                try:
                     # open with firefox
                     print("Recommended installing Mozilla Firefox for a better user experience.")
                     os.system(f'xdg-open {scenarioFile} &')
                except:
                    try:
                        #open in the command line
                        os.system(f'cat {scenarioFile}')
                    except:
                        #if on windows, open in a default desktop program
                        os.system(scenarioFile)
            
            #Open simulation-scenario-bundle folder
            elif "openFolder" in form.keys():
                scenarioFileFolder = os.path.split(scenarioFile)
                #get file from base
                try:
                     os.system(f'xdg-open {scenarioFileFolder[0]} &')
                except:
                    #Not possible to open
                    print("Not possible to open {}".format(scenarioFileFolder[0]))

            #Call EXPORT function to transform scenario-bundle from HOOP in
            #WhatIf compatible format
            elif "exportHoopScenarioFile" in form.keys():
                #Use function from OrchestratorFile
                self.name         = "HOOPSIM-STANDALONE"
                self.blockOnFatal = True
                self.exportSimulationScenarioBundle(HOOPscenarioFile, outputFolder, HOOPscenarioCompatibleFileName)
             
            #Open HOOP simulation-scenario-bundle folder
            elif "openFolderHOOPInput" in form.keys():
                scenarioFileFolder = os.path.split(HOOPscenarioFile)
                #get file from base
                try:
                     os.system(f'xdg-open {scenarioFileFolder[0]} &')
                except:
                    #Not possible to open
                    print("Not possible to open {}".format(scenarioFileFolder[0]))
                
            elif "kibanaOutput" in form.keys():

                #################################
                #Open KIBANA Elasticsearch output
                #################################

                #Open KIBANA
                openIndexURL    = 'https://search-hoopsim-xebvo4edd36kgunyxhaxct2tqi.eu-central-1.es.amazonaws.com/_plugin/kibana/app/management/kibana/indexPatterns'
                openDiscoverURL = 'https://search-hoopsim-xebvo4edd36kgunyxhaxct2tqi.eu-central-1.es.amazonaws.com/_plugin/kibana/app/discover#/'
                # open with Firefox
                print("Recommended installing Mozilla Firefox for a better user experience.")
                os.system(f'xdg-open {openDiscoverURL} &')

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
