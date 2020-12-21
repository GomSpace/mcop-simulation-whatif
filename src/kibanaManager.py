#! /usr/bin/env python3

""" Call ElasticSearch AWS """

import os, signal
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

    def createIndex(self, indexESName, indexConfigFile) ->None:
        '''createIndex
            Create Index Pattern in ElasticSearch
        '''
        # indexConfigFile   = 'index_hoopsim.json'
        apostr = "'"

        curl = f'curl -vs -X PUT {apostr}{self.host}/{indexESName}{apostr} -H {apostr}Content-Type: application/json{apostr} -d @{indexConfigFile}'
        os.system(curl)

    
    def main(self,  outputPath : str, 
                    scenarioFile: str, 
                    indexESName: str,
                    indexConfigFile: str) -> None:
        """ The AWSKibanaHandler will perform following tasks:
            - check if the output folder contains results
            - call AWS service
            - convert .out files into ES compatible dictionary and send to AWS Kibana
            
            return False if failed
        """
        
        #Initialize AWS service
        self.initializeService()

        #Get scenario output name
        with open(scenarioFile) as scenarioJson:
            scenarioData = json.load(scenarioJson)

        #Try to create index (useful for the first time)
        self.createIndex(indexESName, indexConfigFile)

        #Send results to Elasticsearch
        self.sendResultsES(outputPath, scenarioData, indexESName)


    def sendResultsES(self, outputPath, scenarioData, indexESName) -> None:
        '''sendResultsES
            Send and visualise the simulation results to/in Kibana ElasticSearch.
            For every result stored in output/ElasticSearch file, send .json 
            sections using the elasticsearch python library
        '''

        scenarioId = scenarioData['simulation']['id']
        outputPath = outputPath + 'sim' + scenarioId

        ESFilesLocation = outputPath + '/ElasticSearch/'

        for ESFile in os.listdir(ESFilesLocation):
            with open(ESFilesLocation + ESFile, "r") as jsonFile:
                EScontent = json.load(jsonFile)

                #Send to AWS ES service each report
                fileId = ESFile.lower()
                fileId = fileId.replace('.json', '')
                fileId = f'{scenarioId}-{fileId}'

                #Count to differenciate the IDs
                count = 0
                for ESblock in EScontent:
                    print('sending...')
                    count += 1
                    self.es.index(index=indexESName, doc_type="_doc", id=f'{fileId}-{count}', body=ESblock)
                    print('\n')
