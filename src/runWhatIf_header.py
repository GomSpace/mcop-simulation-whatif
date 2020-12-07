#! /usr/bin/env python3

import subprocess
import http.server

import cgi


################################################################################
#Import working folders
import os

rootFolder           = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

utilsFolder         = os.path.join(os.path.dirname(rootFolder),   #../mcop-simulation-federates/util
                                                  'mcop-simulation-federates', 'util')
orchestratorFolder  = os.path.join(os.path.dirname(rootFolder),   #../mcop-simulation-federates/sim_orchestrator/src
                                                  'mcop-simulation-federates', 
                                                  'sim_orchestrator', 'src')
runSimulationFolder = os.path.join(os.path.dirname(rootFolder),   #../mcop-simulation-platform/src
                                                  'mcop-simulation-platform', 'src')

#Add to PYTHONPATH
relativePath = [str(utilsFolder), str(orchestratorFolder), str(runSimulationFolder)]
paths = ":".join(relativePath)
print(paths)
#Add the relative paths to the PYTHONPATH
os.environ["PYTHONPATH"] = ""
os.environ["PYTHONPATH"] = paths + ":" + ("" if os.environ.get("PYTHONPATH") == None else os.environ.get("PYTHONPATH"))
print(os.environ["PYTHONPATH"] )



################################################################################
#Import ORCHESTRATOR file managment
from orchestratorFile import OrchestratorFile

# This class will handles any incoming request from
# the browser 
# It is derived from BaseHTTPRequestHandler
class ServerHandler(http.server.BaseHTTPRequestHandler, OrchestratorFile):
    
	 #Handler for the GET requests
    def do_GET(self):
        self.path = ("./src/webGateway.html")

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
            self.send_error(404,'File Not Found: %s' % self.path)
            
    #Handler for the POST requests
    def do_POST(self):
        if self.path=="/send":
            form = cgi.FieldStorage(fp=self.rfile, 
                                    headers=self.headers,
                                    environ={'REQUEST_METHOD': 'POST',
                                    'CONTENT_TYPE': (self.headers['Content-Type']),})
            
            self.send_response(200)
            self.end_headers()            
            
            #Read form the main window the value
            scenarioFile        = form["scenarioFile"].value
            modemModulationFile = form["modemModulationFile"].value
            outputFolder        = form["outputFolder"].value
            periodicUpdate      = form["periodicUpdate"].value
            
            HOOPscenarioFile    = form["HOOPscenarioFile"].value
            
            #Default argument
            name = "whatIf"
            elevationAngleStep = 0.01 #[deg]
            fedName = "HOOPSIM_{}".format(name)
            simulationClassList = "['pcdu','solararr','batt','payload','storageunit','receiver','transmitter','transceiver']"

#             self.args.fomFName = form["fomFName"].value
#             self.args.fomPName = form["fomPName"].value
#             self.args.inputsPName = form["inputsPName"].value
#             self.args.modelsPName = form["modelsPName"].value
#             self.args.outputsPName = form["outputsPName"].value
#             self.args.runtimePName = form["runtimePName"].value
#             self.args.nSats = form["nSats"].value
#             self.args.deltaTime = form["deltaTime"].value
#             self.args.lookAhead = form["lookAhead"].value
#             self.args.evt_detect_threshold = form["evt_detect_threshold"].value
#             self.args.sim_latency_mean = form["sim_latency_mean"].value
#             self.args.sim_latency_dev = form["sim_latency_dev"].value
#             self.args.insolation_prep = form["insolation_prep"].value
             
            #Run the simulation with the defined arguments
            if "RUN SIMULATION" in form.keys():
                subprocess.Popen(['xterm', '-fa', 'Monospace', '-fs', '14',
                                  '-hold', '-l', '-geometry', '-0+0',
                                  '-title', 'RUN SIMULATION', '-e',
                                  'cd ' + runSimulationFolder + ' && runSimulation.py && cd -',
                                  '--scenarioFile',        scenarioFile,
                                  '--modemModulationFile', modemModulationFile,
                                  '--outputFolder',        outputFolder,
                                  '--periodicUpdate',      periodicUpdate,
                                  '--name',                name,
                                  '--elevationAngleStep',  elevationAngleStep,
                                  '--fedName',             fedName,
                                  '--simulationClassList', simulationClassList])
                       
            #Call EXPORT function to transform scenario-bundle from HOOP in
            #WhatIf compatible format
            elif "EXPORT" in form.keys():
                #Use function from OrchestratorFile
                self.exportSimulationScenarioBundle(HOOPscenarioFile, scenarioFile)
            
            #Open simulation-scenario-bundle in a new tab
            elif "OPEN scenarioFile" in form.keys():
                pass
              #??  htmlfile.write('<a href = " 'fruit+'.html" target="_blank"> '+fruit+'</a><br>\n')
                
                
            #Call the output in KIBANA
            elif "KIBANA OUTPUT" in form.keys():
                pass
                 
#             if "RTI" in form.keys():
#                 # maybe replaced by ayncio in next versions
#                 # https://stackoverflow.com/questions/16071866/non-blocking-subprocess-call
#                 oldDir = getcwd()
#                 copyfile(self.args.fomPName + sep + self.args.fomFName,
#                          self.args.runtimePName + sep + self.args.fomFName)
#                 subprocess.Popen(['xterm', '-fa', 'Monospace', '-fs', '14',
#                                   '-hold', '-l', '-geometry', '-0+0',
#                                   '-title', 'CERTI', '-e',
#                                   'cd ' + self.args.runtimePName
#                                   + ' && rtig'])
#                 chdir(oldDir)
#                 print('RTI launched.')
#             elif "UAV-RECEIVE_F" in form.keys():
#                 print('uav-receive.py federate launched.')
#                 subprocess.Popen(['xterm', '-fa', 'Monospace', '-fs', '14',
#                                    '-hold', '-l', '-e',
#                                    'cd src && python2 uav-receive.py'])
#             elif "UAV-SEND_F" in form.keys():
#                 print('uav-send.py federate launched.')
#                 subprocess.Popen(['xterm', '-fa', 'Monospace', '-fs', '14',
#                                   '-hold', '-l', '-e',
#                                   'cd src && python2 uav-send.py'])
#             elif "EXECTRL_F" in form.keys():
#                 print('exectrl.py federate launched.')
#                 subprocess.Popen(['xterm', '-fa', 'Monospace', '-fs', '14',
#                                   '-hold', '-l', '-geometry', '-0-0',
#                                   '-title', 'EXECRTL_F', '-e',
#                                   'cd src && python3 exectrl_f.py --deltatime '
#                                   + self.args.deltaTime
#                                   + ' --lookahead ' + self.args.lookAhead])
#             elif "OBDSIM_F" in form.keys():
#                 print('obdsim.py federate launched.')
#                 subprocess.Popen(['xterm', '-fa', 'Monospace', '-fs', '14',
#                                   '-hold', '-l', '-bg', 'gold1', '-fg',
#                                   'black', '-geometry', '+0+0',
#                                   '-title', 'OBDSIM_F', '-e',
#                                   'cd src && python3 obdsim_f.py --deltatime '
#                                   + self.args.deltaTime
#                                   + ' --lookahead ' + self.args.lookAhead
#                                   + ' --evt_detect_threshold '
#                                   + self.args.evt_detect_threshold
#                                   + ' --sim_latency_mean '
#                                   + self.args.sim_latency_mean
#                                   + ' --sim_latency_dev '
#                                   + self.args.sim_latency_dev])
#             elif "BATSIM_F" in form.keys():
#                 print('batsim.py federate launched.')
#                 subprocess.Popen(['xterm', '-fa', 'Monospace', '-fs', '14',
#                                   '-hold', '-l', '-bg', 'darkgreen', '-fg',
#                                   'lightblue', '-geometry', '+0-0',
#                                   '-title', 'BATSIM_F', '-e',
#                                   'cd src && python3 batsim_f.py --deltatime '
#                                   + self.args.deltaTime
#                                   + ' --lookahead ' + self.args.lookAhead])
#             elif "ORBSIM_F" in form.keys():
#                 print('orbsim.py federate launched.')
#                 subprocess.Popen(['xterm', '-fa', 'Monospace', '-fs', '14',
#                                   '-hold', '-l', '-bg', 'darkred', '-fg',
#                                   'lightblue', '-geometry', '+0-0',
#                                   '-title', 'ORBSIM_F', '-e',
#                                   'cd src && java -jar orbsim_f-0.0.1.jar'])
            else:
                self.assassin.start()

            return
         
# -*- coding: utf-8 -*-

