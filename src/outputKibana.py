#! /usr/bin/env python3

""" Call ElasticSearch AWS """

import os
import glob
from pathlib import Path
import json
import csv
from threading import Thread
import subprocess

#Import ES library
from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
import boto3

#Establish Paths to Folders
import simImports

# #Import ORCHESTRATOR file managment
from orchestratorFile import OrchestratorFile

class AWSKibanaHandler(OrchestratorFile):
    
    def initializeService(self) -> None:
        """initializeService
            Initalzie AWS service
        """
        #Define AWS host
        self.host = 'https://search-hoopsim-xebvo4edd36kgunyxhaxct2tqi.eu-central-1.es.amazonaws.com'
        region = 'eu-central-1'
        
        #Define the service
        service = 'es'
        credentials = boto3.Session().get_credentials()
        awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)
        
        try:
            self.es = Elasticsearch( hosts = [self.host], #{'host': host, 'port': 443}
                                        http_auth = awsauth,
                                        use_ssl = True,
                                        verify_certs = True,
                                        connection_class = RequestsHttpConnection
                                    )


        except:
            print('Connection with Server was not established')

    def createIndex(self) ->None:
        '''createIndex
            Create Index Pattern in ElasticSearch
        '''
        print(dir(self.es.index))

        indexESName = 'hoopsim'
        indexFile   = 'index_hoopsim.json'

        try:
            curl = f'curl -vs -X PUT {self.host}/{indexESName}* -H Content-Type: application/json -d @{indexFile}'
            os.system(curl)
            print('index pattern is created')
        except:
            print('index pattern was already created')

    
    def main(self, outputPath : str, scenarioFile: str) -> bool:
        """ The AWSKibanaHandler will perform following tasks:
            - check if the output folder contains results
            - call AWS service
            - convert .out files into ES compatible dictionary and send to AWS Kibana
            
            return False if failed
        """
        
        #Initialize AWS service
        self.initializeService()
        self.createIndex()

        #Get scenario output name
        scenarioData = self.getScenarioData(scenarioFile)
        scenarioId = scenarioData['simulation']['id']
        outputPath = outputPath + 'sim' + scenarioId #outputPath + "/" + scenarioId

        ESFilesLocation = outputPath + '/ElasticSearch/'
        print('ESFilesLocation', ESFilesLocation)

        for ESFile in os.listdir(ESFilesLocation):
            with open(ESFilesLocation + ESFile, "r") as jsonFile:
                EScontent = json.load(jsonFile)
                # EScontent = csv.reader(jsonFile)
                # print(EScontent)
                # input()
                #Send to AWS ES service each report
                indexId = ESFile.lower()
                indexId = indexId.replace('.json', '')
                # indexId = indexId.replace('.out', '')
                for ESblock in EScontent:
                    self.es.index(index=f"hoopsim", doc_type="_doc", id=indexId, body=ESblock)
                    print('\n')
