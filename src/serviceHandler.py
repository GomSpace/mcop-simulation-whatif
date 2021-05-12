#! /usr/bin/env python3

import http.server
import os
import signal

#Import glob
from glob import glob

#This module defines a number of utilities for use by CGI scripts written in Python.
import cgi

#Import project folders
import importSimProject

#Import the modules needed in this script
from logger           import Logger
from orchestratorFile import OrchestratorFile


#################################
#TODO add visualization of last simulation-report
#TODO add expandable section for part with periodicupdate, modemfile, etc
#TODO proper kill when click on close tab
#TODO set files from borwser

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

        self.path = ("HOOPSIMui.html")
       
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
            scenarioFile                   = os.path.join(rootDirPath, form["scenarioFile"].value)
            modemModulationFile            = os.path.join(rootDirPath, form["modemModulationFile"].value)
            SOC_OCVbattFile                = os.path.join(rootDirPath, form["SOC_OCVbattFile"].value)
            outputPath                     = os.path.join(rootDirPath, form["outputPath"].value)
            periodicUpdate                 = form["periodicUpdate"].value
            HOOPscenarioFile               = os.path.join(rootDirPath, form["HOOPscenarioFile"].value)
            HOOPscenarioCompatibleFileName = form["HOOPscenarioCompatibleFileName"].value
            
            #Default ORCHESTRATOR arguments
            elevationAngleStep  = '0.01' #[deg]
            awsOutput           = 'True'
            runningDeployment   = 'True'
            runningTest         = 'False'
            simulatorName       = "standalone"
            federationName      = f"HOOPSIM_{simulatorName}"
            NmonteCarloRun      = 0
            
            #Run the simulation with the defined arguments
            if "runSimulation" in form.keys():
                
                #Get check button if run thermal model or not
                try:
                    runningThermal  = True if form["thermal"].value == 'on' else False
                except:
                    runningThermal  = False
                    
                #Get check button if run in MonteCarlo multiple runs
                try:
                    runningMonteCarlo  = True if form["monteCarlo"].value == 'on' else False
                    NmonteCarloRun     = form["monteCarloRuns"].value
                except:
                    runningMonteCarlo  = False
                
                orchestratorArguments = ['python3', 
                                         os.path.join(runOrchestratorPath, 'orchestrator.py'),
                                         '--scenarioFile',        scenarioFile,
                                         '--modemModulationFile', modemModulationFile,
                                         '--battOCVSOCFile',      SOC_OCVbattFile,
                                         '--outputPath',          self.outputPath if outputPath == "" else outputPath,
                                         '--periodicUpdate',      periodicUpdate,
                                         '--elevationAngleStep',  elevationAngleStep,
                                         '--fedName',             federationName,
                                         '--name',                simulatorName,
                                         '--awsOutput',           awsOutput,
                                         '--runningThermal',      str(runningThermal),
                                         '--runningMonteCarlo',   str(runningMonteCarlo),
                                         '--runningDeployment',   runningDeployment,
                                         '--runningTest',         runningTest,
                                         '--NmonteCarloRun',      str(NmonteCarloRun),
                                         ]
                os.system(' '.join(orchestratorArguments))
                
                #TODO when visualize 
#                reportFileList = []
#                for directory,_,_ in os.walk(outputPath):
#                    reportFileList.extend(glob(os.path.join(directory, '*report.yaml')))
#                if runningMonteCarlo:
#                    for filePath in reportFileList:
#                        if 'MonteCarloResults' in filePath:
#                            reportFile = filePath
#                else:
#                    reportFile = reportFileList[0]
#                with open(reportFile, 'r') as report:
#                    fileContent = report.read()
#                    form["simulation-report"].value = fileContent
                    

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
            
            #Open output folder
            elif "openOutputFolder" in form.keys():
                #get file from base
                try:
                     os.system(f'xdg-open {outputPath} &')
                except:
                    #Not possible to open
                    print("Not possible to open {}".format(outputPath))

            #Call Convert function to transform scenario-bundle from HOOP in
            #WhatIf compatible format
            elif "convertToRelativeTime" in form.keys():
                #Use function from OrchestratorFile
                self.name         = "HOOPSIM-STANDALONE"
                self.blockOnFatal = True
                self.exportSimulationScenarioBundle(HOOPscenarioFile, outputPath, HOOPscenarioCompatibleFileName)
             
            #Open HOOP simulation-scenario-bundle folder
            elif "openSourceFolder" in form.keys():
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
